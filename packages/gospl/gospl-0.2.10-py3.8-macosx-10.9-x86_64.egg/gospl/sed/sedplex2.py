import os
import gc
import sys
import petsc4py
import numpy as np
import numpy_indexed as npi

from mpi4py import MPI
from time import process_time

if "READTHEDOCS" not in os.environ:
    from gospl._fortran import fillpit
    from gospl._fortran import setmaxnb
    from gospl._fortran import marinediff
    from gospl._fortran import marinecoeff
    from gospl._fortran import mfdreceivers
    from gospl._fortran import buildclosedsea
    from gospl._fortran import buildclosedland
    from gospl._fortran import distributecloseland
    from gospl._fortran import distributeclosesea
    from gospl._fortran import distributeexcesssea
    from gospl._fortran import distributeocean
    from gospl._fortran import sethillslopecoeff

petsc4py.init(sys.argv)
MPIrank = petsc4py.PETSc.COMM_WORLD.Get_rank()
MPIcomm = petsc4py.PETSc.COMM_WORLD


class SEDMesh(object):
    """
    This class encapsulates all the functions related to sediment transport, production and deposition. `gospl` has the ability to track two types of clastic sediment size and one type of carbonate (still under development). The following processes are considered:

    - inland river deposition in depressions
    - marine deposition at river mouth
    - hillslope processes in both marine and inland areas
    - sediment compaction as stratigraphic layers geometry and properties change

    .. note::
        All these functions are ran in parallel using the underlying PETSc library.

    """

    def __init__(self, *args, **kwargs):
        """
        The initialisation of `SEDMesh` class consists in the declaration of several PETSc vectors.
        """

        # Petsc vectors
        self.tmp = self.hGlobal.duplicate()
        self.tmpL = self.hLocal.duplicate()
        self.tmp1 = self.hGlobal.duplicate()
        self.tmp1L = self.hLocal.duplicate()
        self.Qs = self.hGlobal.duplicate()
        self.QsL = self.hLocal.duplicate()
        self.vSed = self.hGlobal.duplicate()
        self.vSedLocal = self.hLocal.duplicate()
        if self.stratNb > 0:
            if self.stratF is not None:
                self.vSedf = self.hGlobal.duplicate()
                self.vSedfLocal = self.hLocal.duplicate()
            if self.stratW is not None:
                self.vSedw = self.hGlobal.duplicate()
                self.vSedwLocal = self.hLocal.duplicate()
            if self.carbOn:
                self.vSedc = self.hGlobal.duplicate()
                self.vSedcLocal = self.hLocal.duplicate()
        maxnb = np.zeros(1, dtype=np.int64)
        maxnb[0] = setmaxnb(self.lpoints)
        MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, maxnb, op=MPI.MAX)
        self.maxnb = maxnb[0]
        self.scaleIDs = np.zeros(self.lpoints)
        self.scaleIDs[self.lIDs] = 1.0

        return

    def getSedFlux(self):
        """
        This function computes sediment flux in cubic metres per year from incoming rivers. Like for the computation of the flow discharge and erosion rates, the sediment flux is solved by an implicit time integration method, the matrix system is the one obtained from the receiver distributions over the unfilled elevation mesh for the flow discharge (`fMat`).

        The PETSc *scalable linear equations solvers* (**KSP**) is used here again with an iterative method obtained from PETSc Richardson solver (`richardson`) with block Jacobian preconditioning (`bjacobi`).
        """

        t0 = process_time()

        # Multi-lithology case
        if self.stratNb > 0:
            # Coarse sediment
            # Get erosion rate (m/yr) to volume
            self.tmpL.setArray(self.thCoarse)
            self.dm.localToGlobal(self.tmpL, self.tmp)
            self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
            # Get the volume of sediment transported in m3 per year
            self._solve_KSP(False, self.fMat, self.tmp, self.vSed)
            # Update local vector
            self.dm.globalToLocal(self.vSed, self.vSedLocal)

            # Fine sediment
            if self.stratF is not None:
                # Get erosion rate (m/yr) to volume
                self.tmpL.setArray(self.thFine)
                self.dm.localToGlobal(self.tmpL, self.tmp)
                self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
                # Get the volume of sediment transported in m3 per year
                self._solve_KSP(False, self.fMat, self.tmp, self.vSedf)
                # Update local vector
                self.dm.globalToLocal(self.vSedf, self.vSedfLocal)

            # Weathered sediment
            if self.stratW is not None:
                # Get erosion rate (m/yr) to volume
                self.tmpL.setArray(self.thClay)
                self.dm.localToGlobal(self.tmpL, self.tmp)
                self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
                # Get the volume of sediment transported in m3 per year
                self._solve_KSP(False, self.fMat, self.tmp, self.vSedw)
                # Update local vector
                self.dm.globalToLocal(self.vSedw, self.vSedwLocal)

            # Carbonate sediment
            if self.carbOn:
                # Get erosion rate (m/yr) to volume
                self.tmpL.setArray(self.thCarb)
                self.dm.localToGlobal(self.tmpL, self.tmp)
                self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
                # Get the volume of sediment transported in m3 per year
                self._solve_KSP(False, self.fMat, self.tmp, self.vSedc)
                # Update local vector
                self.dm.globalToLocal(self.vSedc, self.vSedcLocal)

        else:
            # Get erosion rate (m/yr) to volume
            self.Eb.copy(result=self.tmp)
            self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
            # Get the volume of sediment transported in m3 per year
            self._solve_KSP(False, self.fMat, self.tmp, self.vSed)
            # Update local vector
            self.dm.globalToLocal(self.vSed, self.vSedLocal)

        if MPIrank == 0 and self.verbose:
            print(
                "Update Sediment Load (%0.02f seconds)" % (process_time() - t0),
                flush=True,
            )

        return

    def _matrixDir(self):
        """
        This function defines the transport direction matrix for filled-restricted elevations.

        .. note::

            Each matrix is built incrementally looping through the number of flow direction paths defined by the user. It proceeds by assembling a local Compressed Sparse Row (**CSR**) matrix to a global PETSc matrix.

            When setting up transport direction matrix in PETSc, we preallocate the non-zero entries of the matrix before starting filling in the values. Using PETSc sparse matrix storage scheme has the advantage that matrix-vector multiplication is extremely fast.

        The  matrix coefficients consist of weights (comprised between 0 and 1) calculated based on the number of downslope neighbours and proportional to the slope.

        """

        dirMat = self.zMat.copy()
        indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)
        nodes = indptr[:-1]

        for k in range(0, self.flowDir):
            # Flow direction matrix for a specific direction
            tmpMat = self._matrix_build()
            data = self.lWght[:, k].copy()
            data[self.lRcv[:, k].astype(petsc4py.PETSc.IntType) == nodes] = 0.0
            tmpMat.assemblyBegin()
            tmpMat.setValuesLocalCSR(
                indptr, self.lRcv[:, k].astype(petsc4py.PETSc.IntType), data,
            )
            tmpMat.assemblyEnd()

            # Add the weights from each direction
            dirMat += tmpMat

            tmpMat.destroy()

        del data, indptr, nodes
        gc.collect()

        # Store flow accumulation matrix
        self.dMat = dirMat.transpose().copy()

        dirMat.destroy()

        return

    def hierarchicalSink(self, offshore=False, land=False, limited=False, gZ=None):
        """
        This function defines the depression properties used to evaluate downstream sediment transport. The following three surfaces case are considered:

        1. a completely filled surface starting from the deep offshore regions
        2. a completely filled surface starting from the sea-level position
        3. a filled-limited surface starting from the sea-level position and limited by user defined `sfill` value (to distribute sediment flux)

        In addition, we extract the volume of all depressions based on current elevation, depressionless one and voronoi cell areas. It also stores the spillover vertices indices for each of the depression. It is ran over the global mesh.

        .. note::

            This function uses the **numpy-indexed** library which contains functionality for indexed operations on numpy ndarrays and provides efficient vectorized functionality such as grouping and set operations.

        :arg offshore: boolean to compute sinks and associated parameters for surface 1
        :arg land: boolean to compute sinks and associated parameters for surface 2
        :arg limited: boolean to compute sinks and associated parameters for surface 3
        """

        t0 = process_time()
        # Get current state global elevations...
        if gZ is None:
            hl = self.hLocal.getArray().copy()
            gZ = np.zeros(self.mpoints)
            gZ[self.locIDs] = hl
            gZ[self.outIDs] = -1.0e8
            MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, gZ, op=MPI.MAX)
            self.gZ = gZ.copy()
            self.oldh = gZ.copy()

        # Perform pit filling on process rank 0
        if MPIrank == 0:
            if offshore:
                sFill, sPits = fillpit(-9.0e3, gZ, 1.0e6)
            if land:
                lFill, lPits = fillpit(self.sealevel, gZ, 1.0e6)
            if limited:
                lFill, lPits = fillpit(self.sealevel, gZ, self.sedfill)
        else:
            if offshore:
                sFill = np.zeros(self.mpoints, dtype=np.float64)
                sPits = np.zeros((self.mpoints, 2), dtype=np.int64)
            if land or limited:
                lFill = np.zeros(self.mpoints, dtype=np.float64)
                lPits = np.zeros((self.mpoints, 2), dtype=np.int64)

        if offshore:
            self.sFill = MPI.COMM_WORLD.bcast(sFill, root=0)
            self.sPits = MPI.COMM_WORLD.bcast(sPits, root=0)
            self.sPitID = np.where(self.sPits[self.locIDs, 0] >= 0)[0]
            # Set all nodes below sea-level as sinks
            self.sinkID = np.where(self.sFill < self.sealevel)[0]
            # Find closed seas
            self.closeIDs = np.where(
                (self.sFill > self.sealevel) & (self.gZ < self.sealevel)
            )[0]
            grpSink = npi.group_by(self.sPits[self.closeIDs, 0])
            self.sGrp = grpSink.unique
            self.sIns, self.sOut, self.sVol = buildclosedsea(
                self.gZ, self.sealevel, self.sGrp, self.sPits
            )
            # Define multiple flow directions for filled elevation
            self.sRcv, dist, self.sWght = mfdreceivers(
                self.flowDir, self.inIDs, self.sFill[self.locIDs], -9.0e3
            )

        if land or limited:
            self.lFill = MPI.COMM_WORLD.bcast(lFill, root=0)
            self.lPits = MPI.COMM_WORLD.bcast(lPits, root=0)
            # Define multiple flow directions for filled elevation
            self.lRcv, dist, self.lWght = mfdreceivers(
                self.flowDir, self.inIDs, self.lFill[self.locIDs], self.sealevel
            )
            # Compute pit volumes inland
            grpSink = npi.group_by(self.lPits[:, 0])
            self.lGrp = grpSink.unique
            self.lIns, self.lVol = buildclosedland(
                self.gZ, self.lFill, self.lGrp, self.lPits
            )
            if land:
                self._matrixDir()
            else:
                self.matrixFlow(False)

            # Get global nodes that have no receivers
            sum_weight = np.sum(self.lWght, axis=1)
            tmpw = np.zeros(self.mpoints, dtype=np.float64)
            tmpw[self.locIDs] = sum_weight
            MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, tmpw, op=MPI.MAX)
            self.lnoRcv = tmpw == 0.0

        if MPIrank == 0 and self.verbose:
            print(
                "Get sink information (%0.02f seconds)" % (process_time() - t0),
                flush=True,
            )

        return

    def distributeSediment(self, stype=0):

        t0 = process_time()
        self.hierarchicalSink(True, True, False, None)

        # Define the volume to distribute
        if stype == 0:
            self.vSedLocal.copy(result=self.QsL)
        elif stype == 1:
            self.vSedfLocal.copy(result=self.QsL)
        elif stype == 2:
            self.vSedcLocal.copy(result=self.QsL)
        elif stype == 3:
            self.vSedwLocal.copy(result=self.QsL)
        self.dm.localToGlobal(self.QsL, self.Qs)

        # From the distance to coastline define the upper limit
        # of the shelf to ensure a maximum slope angle
        clinoH = self.sealevel - self.coastDist * self.slps[stype] * 1.0e-5
        tmp = np.zeros(self.mpoints, dtype=np.float64) + 1.0e8
        tmp[self.locIDs] = clinoH
        tmp[self.outIDs] = 1.0e8
        MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, tmp, op=MPI.MIN)
        vdepth = tmp - self.gZ
        vdepth[vdepth < 0.0] = 0.0

        # Get the volumetric sediment rate (m3/yr) to distribute during the time step and convert in volume (m3) for considered timestep
        lQs = self.QsL.getArray().copy()
        nQs = np.zeros(self.mpoints, dtype=np.float64)
        nQs[self.locIDs] = lQs * self.dt
        nQs[self.outIDs] = 0.0
        MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, nQs, op=MPI.MAX)
        Qs = np.zeros(self.mpoints, dtype=np.float64)
        Qs[self.pitPts] = nQs[self.pitPts]
        del nQs

        # Update all flux in the main sink
        sinkFlx = np.zeros(self.mpoints, dtype=np.float64)
        depo = np.zeros(self.mpoints, dtype=np.float64)
        sinkFlx[self.sinkID] += Qs[self.sinkID]
        Qs[self.sinkID] = 0.0

        ins = np.where(Qs > 0)[0]
        if len(ins) == 0:
            # Will need to be modified###
            ###
            return

        step = 0
        while (Qs > 0).any():

            # Check if sediments are in closed sea
            insea = np.where(self.sIns[ins] > -1)[0]

            if len(insea) > 0:
                # Distribute sediments to next sink
                Qs, ndepo, self.sVol, outVol = distributeclosesea(
                    Qs,
                    self.gZ,
                    self.sealevel,
                    self.sGrp,
                    self.sPits,
                    self.sVol,
                    self.sOut,
                )
                depo += ndepo
                self.gZ += ndepo

                # Was the elevation updated? if so update the downstream parameters
                if (depo > 0).any():
                    self.hierarchicalSink(False, True, False, self.gZ)

                # Are there excess sea deposits to distribute?
                if (outVol > 0).any():
                    Qs, ndepo, self.lVol = distributeexcesssea(
                        Qs,
                        self.gZ,
                        self.lFill,
                        self.lPits,
                        self.lVol,
                        outVol,
                        self.sOut,
                        self.lIns,
                    )
                    depo += ndepo
                    self.gZ += ndepo

                # Remove flux that flow into open sea
                sinkFlx[self.sinkID] += Qs[self.sinkID]
                Qs[self.sinkID] = 0.0

            # At this point excess sediments are all in continental regions
            if (Qs > 0).any():
                self.tmpL.setArray(Qs[self.locIDs])
                self.dm.localToGlobal(self.tmpL, self.tmp)
                # Move to the first downstream node
                self.dMat.mult(self.tmp, self.tmp1)

                # Downstream distribution of the excess in continental regions
                self.hierarchicalSink(False, False, True, self.gZ)
                self._solve_KSP(False, self.fMat, self.tmp1, self.tmp)
                self.dm.globalToLocal(self.tmp, self.tmpL)
                nQs = np.zeros(self.mpoints)
                nQs[self.locIDs] = self.tmpL.getArray().copy()
                nQs[self.outIDs] = 0.0
                MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, nQs, op=MPI.MAX)

                Qs = np.zeros(self.mpoints)
                sinkFlx[self.sinkID] += nQs[self.sinkID]
                nQs[self.sinkID] = 0.0
                Qs[self.lnoRcv] = nQs[self.lnoRcv]
                nQs[self.lnoRcv] = 0.0

                # Update sediment volume in streams
                self.tmpL.setArray(nQs[self.locIDs])
                self.vSedLocal.axpy(1.0, self.tmpL)
                self.dm.localToGlobal(self.vSedLocal, self.vSed)

                # Are the fluxes in a continental pit
                if (Qs > 0).any():
                    Qs, ndepo, self.lVol = distributecloseland(
                        Qs, self.gZ, self.lFill, self.lGrp, self.lPits, self.lVol
                    )
                    depo += ndepo
                    self.gZ += ndepo

                if MPIrank == 0:
                    print("sum to distribute 4", np.sum(Qs))

                step += 1
                if step > 2:
                    sinkFlx += Qs
                    break

        if MPIrank == 0 and self.verbose:
            print(
                "Distribute closed seas and land sediments (%0.02f seconds)"
                % (process_time() - t0),
                flush=True,
            )

        # Distribute open sea sediments
        t1 = process_time()
        sid = np.argsort(self.sFill)[::-1]
        tmpw = np.zeros(self.mpoints, dtype=np.float64)
        tmpr = -np.ones(self.mpoints, dtype=int)
        sWght = np.zeros((self.mpoints, self.flowDir), dtype=np.float64)
        sRcv = -np.ones((self.mpoints, self.flowDir), dtype=int)
        for k in range(self.flowDir):
            tmpw[self.locIDs] = self.sWght[:, k]
            tmpw[self.outIDs] = 0.0
            MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, tmpw, op=MPI.MAX)
            sWght[:, k] = tmpw
            val = self.locIDs[self.sRcv[:, k]]
            nrcv = np.where(self.rcvID[:, k] == -1)[0]
            val[nrcv] = -1
            tmpr[self.locIDs] = val
            tmpr[self.outIDs] = -1
            MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, tmpr, op=MPI.MAX)
            sRcv[:, k] = tmpr
        vol = vdepth * self.marea
        ndepo = distributeocean(self.flowDir, sid, sinkFlx, sRcv, sWght, vol, vdepth)

        if (ndepo > 0).any():
            sedK = self.sedimentK
            if sedK > 0.0:
                if stype == 1:
                    sedK = self.sedimentKf
                if stype == 3:
                    sedK = self.sedimentKw

            zb = self.gZ.copy()
            h = self.gZ.copy() + ndepo

            for s in range(5):

                # Diffusion matrix construction
                Cd = np.zeros(self.lpoints, dtype=np.float64)
                Cd[self.seaID] = sedK
                Cd[ndepo[self.locIDs] < 10.0] = 0.5

                diffCoeffs = sethillslopecoeff(self.lpoints, Cd * self.dt)
                seaDiff = self._matrix_build_diag(diffCoeffs[:, 0])
                indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)

                for k in range(0, self.maxnb):
                    tmpMat = self._matrix_build()
                    indices = self.FVmesh_ngbID[:, k].copy()
                    data = diffCoeffs[:, k + 1]
                    ids = np.nonzero(data == 0.0)
                    indices[ids] = ids
                    tmpMat.assemblyBegin()
                    tmpMat.setValuesLocalCSR(
                        indptr, indices.astype(petsc4py.PETSc.IntType), data,
                    )
                    tmpMat.assemblyEnd()
                    seaDiff += tmpMat
                    tmpMat.destroy()

                self.tmp1.setArray(h[self.glbIDs])
                self._solve_KSP(False, seaDiff, self.tmp1, self.tmp)
                self.dm.globalToLocal(self.tmp, self.tmpL)
                hl = self.tmpL.getArray().copy()
                h = np.zeros(self.mpoints)
                h[self.locIDs] = hl
                h[self.outIDs] = -1.0e8
                MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, h, op=MPI.MAX)
                ndepo = h - zb
                ndepo[ndepo < 0.0] = 0.0
                # del ids, indices, indptr, diffCoeffs, Cd
                # gc.collect()

            depo = h - self.oldh
            self.gZ = h

        if MPIrank == 0 and self.verbose:
            print(
                "Diffuse open ocean sediments (%0.02f seconds)" % (process_time() - t1),
                flush=True,
            )

        # Update cumed and elev
        self.tmpL.setArray(depo[self.locIDs])
        self.dm.localToGlobal(self.tmpL, self.tmp)
        self.cumED.axpy(1.0, self.tmp)
        self.hGlobal.axpy(1.0, self.tmp)
        self.dm.globalToLocal(self.cumED, self.cumEDLocal)
        self.dm.globalToLocal(self.hGlobal, self.hLocal)

        del depo, outVol

        if self.stratNb > 0:
            self._deposeStrat(stype)

            if self.stratNb > 0:
                self.erodeStrat()
                self._deposeStrat(stype)

        # del excess, newgQ, dep, scaleV
        # del gQ, Qs, tmp
        # gc.collect()

        return

    def sedChange(self):
        """
        This function is the main entry point to perform both continental and marine river-induced deposition. It calls the private function `_sedChange`.
        """

        # Define points in the marine environment for filled surface
        # self.fillSeaID = np.where(self.hFill <= self.sealevel)[0]

        if self.stratNb > 0:
            self._sedChange(stype=0)
            if self.carbOn:
                self._sedChange(stype=2)
            if self.stratF is not None:
                self._sedChange(stype=1)
            if self.stratW is not None:
                self._sedChange(stype=3)
        else:
            self._sedChange(stype=0)

        return

    def _getSed(self, stype):
        """
        Pick the relevant PETSc array for the specified sediment type.
        """

        if stype == 0:
            self.vSedLocal.copy(result=self.QsL)
        elif stype == 1:
            self.vSedfLocal.copy(result=self.QsL)
        elif stype == 2:
            self.vSedcLocal.copy(result=self.QsL)
        elif stype == 3:
            self.vSedwLocal.copy(result=self.QsL)
        self.dm.localToGlobal(self.QsL, self.Qs)

        return

    def _sedChange(self, stype):
        """
        Deposition in depressions and the marine environments.

        This function contains methods for the following operations:

        - stream induced deposition in depression
        - marine river sediments diffusion
        - carbonate production from fuzzy logic

        .. note::

            When dealing with multiple depressions, the calculation of sediment flux over a landscape needs to be done carefully. The approach proposed here consists in iteratively filling the depressions as the sediment flux is transported downstream. To do so it *(1)* records the volume change in depressions if any, *(2)* updates elevation changes and *(3)* recomputes the flow discharge based on the `FAMesh` class functions.

        Once river sediments have reached the marine environment, a marine sediment-transport equations taking into account the tracking of the two different grain sizes is performed using a linear diffusion equation characterized by distinct transport coefficients.

        """

        # Compute continental sediment deposition
        self.seaQs = np.zeros(self.lpoints, dtype=np.float64)
        self._getSed(stype)

        perc = 1.0
        minperc = 1.0e-4
        iters = 0
        fill = False
        totQs = self.Qs.sum()
        while self.Qs.sum() > 0.0 and iters < 100:
            self._continentalDeposition(stype, filled=fill)
            if perc < minperc:
                self.Qs.set(0.0)
                self.QsL.set(0.0)
            perc = self.Qs.sum() / totQs
            if self.Qs.sum() > 0.0:
                if perc >= minperc and iters < 99:
                    self.flowAccumulation(filled=False, limit=False)
                else:
                    fill = True
                self._moveFluxes(filled=fill)
                iters += 1

            if MPIrank == 0 and self.verbose:
                print(
                    "Remaining percentage to transport: %0.01f %d"
                    % (perc * 100.0, iters),
                    flush=True,
                )

            if stype == 0:
                self.vSedLocal.axpy(1.0, self.QsL)
            if stype == 1:
                self.vSedfLocal.axpy(1.0, self.QsL)
            if stype == 2:
                self.vSedcLocal.axpy(1.0, self.QsL)
            if stype == 3:
                self.vSedwLocal.axpy(1.0, self.QsL)

        if stype == 0:
            self.dm.localToGlobal(self.vSedLocal, self.vSed)
        if stype == 1:
            self.dm.localToGlobal(self.vSedfLocal, self.vSedf)
        if stype == 2:
            self.dm.localToGlobal(self.vSedcLocal, self.vSedc)
        if stype == 3:
            self.dm.localToGlobal(self.vSedwLocal, self.vSedw)

        # Compute Marine Sediment Deposition
        self.dm.localToGlobal(self.hLocal, self.hGlobal)
        self.QsL.setArray(self.seaQs)
        self.dm.localToGlobal(self.QsL, self.Qs)
        sedK = self.sedimentK
        if sedK > 0.0:
            if stype == 1:
                sedK = self.sedimentKf
            if stype == 3:
                sedK = self.sedimentKw
            self._marineDeposition(stype, sedK)

        # Compute Fuzzy Logic Carbonate Growth
        if self.carbOn:
            self._growCarbonates()

        return

    def getHillslope(self):
        r"""
        This function computes hillslope processes. The code assumes that gravity is the main driver for transport and states that the flux of sediment is proportional to the gradient of topography.

        As a result, we use a linear diffusion law commonly referred to as **soil creep**:

        .. math::
          \frac{\partial z}{\partial t}= \kappa_{D} \nabla^2 z

        in which :math:`\kappa_{D}` is the diffusion coefficient and can be defined with different values for the marine and land environments (set with `hillslopeKa` and `hillslopeKm` in the YAML input file). It encapsulates, in a simple formulation, processes operating on superficial sedimentary layers. Main controls on variations of :math:`\kappa_{D}` include substrate, lithology, soil depth, climate and biological activity.
        """

        # Compute Hillslope Diffusion Law
        h = self.hLocal.getArray().copy()
        self.seaID = np.where(h <= self.sealevel)[0]
        self._hillSlope()

        # Update layer elevation
        if self.stratNb > 0:
            self._elevStrat()

        del h
        gc.collect()

        return

    def _growCarbonates(self):
        """
        When carbonates is turned on update carbonate thicknesses based on fuzzy logic controls. The carbonate thicknesses created are uncompacted ones.

        .. warning::

            This function is a place order and will be updated in a future version of `gospl`.
        """

        # Limit fuzzy controllers to possible value range
        hl = self.sealevel - self.hLocal.getArray().copy()

        # TO DO: this will need to be updated with additional controls...
        carbH = np.zeros(self.lpoints, dtype=np.float64)
        validIDs = np.ones(self.lpoints, dtype=np.int64)
        for k in range(len(self.carbCtrl.controlKeys)):
            # Accomodation control
            if self.carbCtrl.controlKeys[k] == "depth":
                ids = np.where(
                    np.logical_or(
                        hl <= self.carbCtrl.controlBounds[k][0],
                        hl >= self.carbCtrl.controlBounds[k][1],
                    )
                )[0]
                validIDs[ids] = 0

        # Compute carbonate growth rates in metres per thousand years
        # and associated thicknesses
        ids = np.where(validIDs > 0)[0]
        for k in range(len(ids)):
            self.carbCtrl.carbControlSystem.input["depth"] = hl[ids[k]]
            # self.carbCtrl.carbControlSystem.input["temperature"] = 20.0
            self.carbCtrl.carbControlSystem.compute()
            growthRate = self.carbCtrl.carbControlSystem.output["growth"]
            carbH[ids[k]] = min(hl[ids[k]] - 1.0e-6, growthRate * self.dt * 1.0e-3)

        # Update top layers based on carbonate growth
        self.tmpL.setArray(carbH)
        self.dm.localToGlobal(self.tmpL, self.tmp)
        self.cumED.axpy(1.0, self.tmp)
        self.hGlobal.axpy(1.0, self.tmp)
        self.dm.globalToLocal(self.cumED, self.cumEDLocal)
        self.dm.globalToLocal(self.hGlobal, self.hLocal)

        if self.stratNb > 0:
            # Update carbonate reef content in the stratigraphic layer
            self._deposeStrat(2)

        del ids, validIDs, carbH, hl
        gc.collect()

        return

    def _moveFluxes(self, filled=False):
        """
        This function updates downstream continental sediment fluxes accounting for changes in elevation induced by deposition.

        As mentionned above, the PETSc *scalable linear equations solvers* (**KSP**) is used here for obtaining the solution.

        :arg filled: boolean to choose between unfilled and filled surface
        """

        t0 = process_time()
        self.Qs.copy(result=self.tmp)

        # Transport sediment volume in m3 per year
        if filled:
            self._solve_KSP(False, self.fillMat, self.tmp, self.Qs)
        else:
            self._solve_KSP(False, self.fMat, self.tmp, self.Qs)

        # Update local vector
        self.dm.globalToLocal(self.Qs, self.QsL)

        if MPIrank == 0 and self.verbose:
            print(
                "Move Sediment Downstream (%0.02f seconds)" % (process_time() - t0),
                flush=True,
            )

        return

    def _continentalDeposition(self, stype, filled=False):
        """
        Accounting for available volume for deposition in each depression, this function records  the amount of sediment deposited inland and update the stratigraphic record accordingly.

        For each sediment type, freshly deposits are given the surface porosities given in the input file.

        If a depression is overfilled the excess sediment is added to the overspill node of the considered depression and is subsequently transported downstream in a subsequent iteration.

        During a given time step, the process described above will be repeated iteratively until all sediment transported are either deposited in depressions or are reaching the shoreline.

        :arg stype: sediment type (integer)
        :arg filled: boolean to choose between unfilled and filled surface
        """

        t0 = process_time()

        # Get the volumetric sediment rate (m3 / yr) to distribute
        # during the time step
        tmp = self.QsL.getArray().copy()

        # Convert in volume (m3) for considered timestep
        # We only consider the nodes that are their own receivers
        Qs = np.zeros(self.lpoints, dtype=np.float64)
        Qs[self.pitPts] = tmp[self.pitPts] * self.dt

        # To avoid counting twice the volume on the partition
        # boundaries we removed ghost nodes volumes
        Qs = np.multiply(Qs, self.scaleIDs)

        # Do not take ocean nodes they will be updated later
        self.seaQs[self.fillSeaID] += Qs[self.fillSeaID] / self.dt
        Qs[self.fillSeaID] = 0.0

        # In case we are using the filled topography all continental rivers
        # drain into the ocean, therefore we can leave the function.
        if filled:
            return

        # Get the sediment volume available for transport and deposition
        # globally
        gQ = Qs[self.lgIDs]
        gQ[self.outIDs] = 0.0
        MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, gQ, op=MPI.MAX)

        # Find sediment load originally in a depression which are now
        # able to flow downslope
        ids = np.where(np.logical_and(self.pits[:, 0] == -1, gQ > 0))[0]
        newgQ = np.zeros(self.mpoints, dtype=np.float64)
        newgQ[ids] = gQ[ids]
        gQ[ids] = 0.0

        # Get the cumulative volume for each depression
        groupPits = npi.group_by(self.pits[:, 0])
        outNb, depFill = groupPits.sum(gQ)

        # Add the excess volume for each pit that needs to be distributed
        excess = np.where(depFill - self.pitVol > 0.0)[0]
        newgQ[self.outFlows[excess]] += depFill[excess] - self.pitVol[excess]
        newQs = newgQ[self.locIDs]

        # Scale the deposition based on available volume
        with np.errstate(divide="ignore", over="ignore"):
            scaleV = np.divide(
                depFill,
                self.pitVol,
                out=np.zeros_like(self.pitVol),
                where=self.pitVol != 0,
            )
        scaleV[scaleV > 1.0] = 1.0

        # Update available volume on each pit
        self.pitVol -= depFill
        self.pitVol[self.pitVol < 0.0] = 0.0

        # Deposit sediment in depressions based on the volumetric scaling
        h = self.hLocal.getArray().copy()
        dep = (self.hFill - h) * scaleV[self.locIDs]

        # Update PETSc vectors
        self.QsL.setArray(newQs / self.dt)
        self.dm.localToGlobal(self.QsL, self.Qs)

        self.tmpL.setArray(dep)
        self.dm.localToGlobal(self.tmpL, self.tmp)
        self.cumED.axpy(1.0, self.tmp)
        self.hGlobal.axpy(1.0, self.tmp)
        self.dm.globalToLocal(self.cumED, self.cumEDLocal)
        self.dm.globalToLocal(self.hGlobal, self.hLocal)

        if self.stratNb > 0:
            self._deposeStrat(stype)

        del newQs, excess, newgQ, dep, h, scaleV, groupPits
        del gQ, ids, Qs, tmp, outNb, depFill
        gc.collect()

        if MPIrank == 0 and self.verbose:
            print(
                "Compute Continental Deposition (%0.02f seconds)"
                % (process_time() - t0),
                flush=True,
            )

        return

    def _nonlinearMarineDiff(self, base, sedK):
        """
        Non-linear diffusion dependent on thicknesses of freshly deposited sediment in the marine realm is solved implicitly using a Picard iteration approach.

        Sediments transported is limited by the underlying bathymentry. Depending on the user defined diffusion coefficients and time-steps a small portion of the underlying bedrock might be eroded during the process...

        :arg base: numpy array representing local basement elevations
        :arg sedK: sediment diffusion coefficient for river transported sediment in the marine realm
        """

        err = 1.0e8
        error = np.zeros(1, dtype=np.float64)

        # Specify the elevation defined by the sum of basement plus
        # marine sediment flux thickness as hOld
        hOld = self.tmp1L.getArray().copy()

        # Update non-linear diffusion coefficients iteratively until convergence
        step = 0
        while err > 1.0e-2 and step < 10:

            # Get marine diffusion coefficients
            diffCoeffs = marinediff(
                self.lpoints, base, hOld, sedK * self.dt, self.sealevel
            )

            # Build the diffusion matrix
            self.Diff = self._matrix_build_diag(diffCoeffs[:, 0])
            indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)

            for k in range(0, self.maxnb):
                tmpMat = self._matrix_build()
                indices = self.FVmesh_ngbID[:, k].copy()
                data = diffCoeffs[:, k + 1]
                ids = np.nonzero(data == 0.0)
                indices[ids] = ids
                tmpMat.assemblyBegin()
                tmpMat.setValuesLocalCSR(
                    indptr, indices.astype(petsc4py.PETSc.IntType), data,
                )
                tmpMat.assemblyEnd()
                self.Diff += tmpMat
                tmpMat.destroy()
            del ids, indices, indptr, diffCoeffs
            gc.collect()

            # Get diffused values for considered time step and diffusion coefficients
            if step == 0:
                self._solve_KSP(False, self.Diff, self.tmp1, self.tmp)
            else:
                self._solve_KSP(True, self.Diff, self.tmp1, self.tmp)

            # Get global error
            self.dm.globalToLocal(self.tmp, self.tmpL)
            newH = self.tmpL.getArray().copy()
            newH[newH < base] = base[newH < base]
            hOld[hOld < base] = base[hOld < base]

            error[0] = np.max(np.abs(newH - hOld)) / np.max(np.abs(newH))
            MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, error, op=MPI.MAX)
            err = error[0]
            self.tmpL.setArray(newH)
            self.dm.localToGlobal(self.tmpL, self.tmp)
            step += 1

            # Update sedH and old elevation values
            self.tmp.copy(result=self.tmp1)
            self.dm.globalToLocal(self.tmp1, self.tmp1L)
            hOld = self.tmp1L.getArray().copy()

        del newH
        gc.collect()

        return hOld

    def _updateMarineDiff(self, nsedK):
        """
        The diffusion equation for fluvial related sediment entering the marine realm is increased when specific convergence iteration numbers are reached to speed up underwater accumulation.

        :arg nsedK: sediment diffusion coefficient for river transported sediment in the marine realm
        """

        # Diffusion matrix construction
        Cd = np.zeros(self.lpoints, dtype=np.float64)
        Cd[self.fillSeaID] = nsedK

        diffCoeffs = marinecoeff(self.lpoints, Cd * self.dt)
        self.Diff = self._matrix_build_diag(diffCoeffs[:, 0])
        indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)

        for k in range(0, self.maxnb):
            tmpMat = self._matrix_build()
            indices = self.FVmesh_ngbID[:, k].copy()
            data = diffCoeffs[:, k + 1]
            ids = np.nonzero(data == 0.0)
            indices[ids] = ids
            tmpMat.assemblyBegin()
            tmpMat.setValuesLocalCSR(
                indptr, indices.astype(petsc4py.PETSc.IntType), data,
            )
            tmpMat.assemblyEnd()
            self.Diff += tmpMat
            tmpMat.destroy()
        del ids, indices, indptr, diffCoeffs, Cd
        gc.collect()

        return

    def _marineDeposition(self, stype, sedK):
        """
        For sediment reaching the coastline, this function computes the related marine
        deposition. The approach is based on a linear diffusion which is applied iteratively
        over a given time step until all the sediment have been diffused.

        The diffusion equation is ran for the coarser sediment first and for the finest one
        afterwards. This mimicks the standard behaviour observed in stratigraphic architectures
        where the fine fraction are generally transported over longer distances.

        The diffusion process stops when the sediment entering the ocean at river mouths are
        distributed and the accumulations on these specific nodes remains below water depth.

        :arg stype: sediment type (integer)
        :arg sedK: sediment diffusion coefficient for river transported sediment in the marine realm
        """

        t0 = process_time()

        # Get the marine volumetric sediment rate (m3 / yr) to diffuse
        # during the time step as suspended material...
        tmp = self.QsL.getArray().copy()
        Qs = np.zeros(self.lpoints, dtype=np.float64)

        # Convert in volume (m3) for considered timestep
        Qs[self.fillSeaID] = tmp[self.fillSeaID] * self.dt

        # Diffusion matrix construction
        Cd = np.zeros(self.lpoints, dtype=np.float64)
        Cd[self.fillSeaID] = sedK

        # From the distance to coastline define the upper limit
        # of the shelf to ensure a maximum slope angle
        if self.vtkMesh is not None:
            toplimit = self.sealevel - self.coastDist * self.slps[stype] * 1.0e-5
        else:
            toplimit = np.full((self.lpoints), 0.9 * self.sealevel)
        toplimit[self.fillSeaID] = np.maximum(
            toplimit[self.fillSeaID], self.hFill[self.fillSeaID]
        )
        self.fillLandID = np.where(self.hFill > self.sealevel)[0]
        toplimit[self.fillLandID] = self.hFill[self.fillLandID]

        # Define maximum deposition thicknesses and initialise
        # cumulative deposits
        h0 = self.hLocal.getArray().copy()
        self.hGlobal.copy(result=self.tmp1)
        self.hLocal.copy(result=self.tmp1L)
        maxDep = toplimit - h0
        maxDep[maxDep < 0.0] = 0.0
        cumDep = np.zeros(self.lpoints, dtype=np.float64)

        # Build suspended sediment volume per unit area (m) vector
        self.tmpL.setArray(Qs)
        self.dm.localToGlobal(self.tmpL, self.Qs)
        maxSedVol = self.Qs.sum()
        self.Qs.pointwiseDivide(self.Qs, self.areaGlobal)

        diffCoeffs = marinecoeff(self.lpoints, Cd * self.dt)
        self.Diff = self._matrix_build_diag(diffCoeffs[:, 0])
        indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)

        for k in range(0, self.maxnb):
            tmpMat = self._matrix_build()
            indices = self.FVmesh_ngbID[:, k].copy()
            data = diffCoeffs[:, k + 1]
            ids = np.nonzero(data == 0.0)
            indices[ids] = ids
            tmpMat.assemblyBegin()
            tmpMat.setValuesLocalCSR(
                indptr, indices.astype(petsc4py.PETSc.IntType), data,
            )
            tmpMat.assemblyEnd()
            self.Diff += tmpMat
            tmpMat.destroy()
        del ids, indices, indptr, diffCoeffs, Cd
        gc.collect()

        iters = 0
        nsedK = sedK
        guess = False
        remainPerc = 1.0
        while (
            iters < 1000 and remainPerc > max(0.005, self.frac_fine) and maxSedVol > 0.0
        ):

            # Get diffused values for considered time step
            if not guess:
                self._solve_KSP(False, self.Diff, self.Qs, self.tmp)
                guess = True
            else:
                self._solve_KSP(True, self.Diff, self.Qs, self.tmp)

            # Find overfilled nodes
            self.dm.globalToLocal(self.tmp, self.tmpL)
            dH = self.tmpL.getArray().copy()
            dH[dH < 0] = 0.0
            overDep = dH - maxDep
            overDep[overDep < 0] = 0.0
            overIDs = np.where(dH > maxDep)[0]

            # Update space both for cumulative and available depths
            cumDep += dH
            cumDep[overIDs] = toplimit[overIDs] - h0[overIDs]
            cumDep[cumDep < 0] = 0.0
            maxDep -= dH
            maxDep[maxDep < 0] = 0.0

            # Update sediment to diffuse
            Qs.fill(0.0)
            Qs[overIDs] = overDep[overIDs]

            # Update PETSc vector
            self.tmpL.setArray(Qs)
            self.dm.localToGlobal(self.tmpL, self.Qs)

            self.Qs.pointwiseMult(self.Qs, self.areaGlobal)
            sedVol = self.Qs.sum()
            remainPerc = sedVol / maxSedVol

            iters += 1
            # Update diffusion coefficient matrix
            if iters % 25 == 0:

                guess = False
                dH = h0 + cumDep

                gZ = np.zeros(self.mpoints)
                gZ[self.locIDs] = dH
                gZ[self.outIDs] = -1.0e8
                MPI.COMM_WORLD.Allreduce(MPI.IN_PLACE, gZ, op=MPI.MAX)
                if MPIrank == 0:
                    hFill, pits = fillpit(self.sealevel - 1000.0, gZ, 1.0e8)
                else:
                    hFill = np.zeros(self.mpoints, dtype=np.float64)
                hFill = MPI.COMM_WORLD.bcast(hFill, root=0)
                hFill = hFill[self.locIDs]
                hFill = np.maximum(hFill, toplimit)

                # Distribute excess sediment volume by moving it on the
                # new surface
                ids = np.where(np.logical_and(hFill > dH, hFill < self.sealevel))[0]
                hFill[ids] = -1.1e6

                # Define the new elevation to diffuse with the excess
                # volume pushed on the edges of the clinoforms
                self._moveMarineSed(hFill)

                if iters % 25 == 0 and nsedK / sedK < 1.0e3:
                    nsedK = nsedK * 10.0
                    self._updateMarineDiff(nsedK)
            else:
                self.Qs.pointwiseDivide(self.Qs, self.areaGlobal)
                self.dm.globalToLocal(self.Qs, self.QsL)

            if iters >= 1000 and MPIrank == 0:
                print(
                    "Sediment marine diffusion not converging; decrease time step or increase sedK",
                    flush=True,
                )

            if MPIrank == 0 and self.verbose:
                print(
                    "Remaining percentage to diffuse: %0.01f " % (remainPerc * 100.0),
                    flush=True,
                )

        # Diffuse deposited sediment
        if maxSedVol > 0.0:
            cumDep[cumDep < 0] = 0.0
            self.tmpL.setArray(cumDep)
            self.dm.localToGlobal(self.tmpL, self.tmp)
            self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
            maxSedVol = self.tmp.sum()
            self.tmp.pointwiseDivide(self.tmp, self.areaGlobal)
            self.tmp1.axpy(1.0, self.tmp)
            self.dm.globalToLocal(self.tmp1, self.tmp1L)
            # step = 0
            # while step < 1:
            dH = self._nonlinearMarineDiff(h0, sedK)
            self.tmp1L.setArray(dH)
            self.dm.localToGlobal(self.tmp1L, self.tmp1)
            # step += 1

            # Update cumulative erosion/deposition and elevation
            cumDep = self.tmp1L.getArray().copy() - h0
            cumDep[cumDep < 0] = 0.0

            # Ensure volume conservation
            self.tmpL.setArray(cumDep)
            self.dm.localToGlobal(self.tmpL, self.tmp)
            self.tmp.pointwiseMult(self.tmp, self.areaGlobal)
            sedVol = self.tmp.sum()
            if sedVol > maxSedVol:
                self.tmp.scale(maxSedVol / sedVol)
                self.tmp.pointwiseDivide(self.tmp, self.areaGlobal)
                self.dm.globalToLocal(self.tmp, self.tmpL)
            else:
                self.tmp.pointwiseDivide(self.tmp, self.areaGlobal)

            self.dm.localToGlobal(self.tmpL, self.tmp)
            self.cumED.axpy(1.0, self.tmp)
            self.hGlobal.axpy(1.0, self.tmp)
            self.dm.globalToLocal(self.cumED, self.cumEDLocal)
            self.dm.globalToLocal(self.hGlobal, self.hLocal)

        if self.stratNb > 0:
            self._deposeStrat(stype)

        del h0, cumDep, maxDep, Qs, toplimit
        if maxSedVol > 0.0:
            del dH, overDep
        if iters > 25:
            del ids, hFill, gZ
        gc.collect()

        if MPIrank == 0 and self.verbose:
            print(
                "Compute Marine Sediment Diffusion (%0.02f seconds)"
                % (process_time() - t0),
                flush=True,
            )

        return

    def _moveMarineSed(self, h):
        """
        This function moves downstream river sediment fluxes based on clinorform slopes
        accounting for changes in elevation induced by marine deposition.

        Here again, the PETSc *scalable linear equations solvers* (**KSP**) is used
        to obtain the solution.

        :arg h: numpy array representing filled elevations up to maximum clinoforms heights
        """

        t0 = process_time()

        # Define multiple sediment distributions
        sedDir = 1
        rcvID, distRcv, wghtVal = mfdreceivers(sedDir, self.inIDs, h, -1.0e6)

        # Get recievers
        rcID = np.where(h <= -1.0e6)[0]

        # Set marine nodes
        rcvID[rcID, :] = np.tile(rcID, (sedDir, 1)).T
        distRcv[rcID, :] = 0.0
        wghtVal[rcID, :] = 0.0

        self.Qs.copy(result=self.tmp)

        sedMat = self.iMat.copy()
        indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)
        nodes = indptr[:-1]

        for k in range(0, sedDir):

            # Flow direction matrix for a specific direction
            tmpMat = self._matrix_build()
            data = -wghtVal[:, k].copy()
            data[rcvID[:, k].astype(petsc4py.PETSc.IntType) == nodes] = 0.0
            tmpMat.assemblyBegin()
            tmpMat.setValuesLocalCSR(
                indptr, rcvID[:, k].astype(petsc4py.PETSc.IntType), data,
            )
            tmpMat.assemblyEnd()

            # Add the weights from each direction
            sedMat += tmpMat
            tmpMat.destroy()

        del data, indptr, nodes, rcvID, distRcv, wghtVal
        gc.collect()

        # Transport sediment volume in m3
        self._solve_KSP(False, sedMat.transpose(), self.tmp, self.Qs)

        # Update local vector
        self.dm.globalToLocal(self.Qs, self.QsL)

        sedMat.destroy()

        # Remaining sediment volumes on the edges of the clinoforms
        tmp = self.QsL.getArray().copy()
        data = np.zeros(len(tmp))
        data[rcID] = tmp[rcID]
        self.QsL.setArray(data)
        self.dm.localToGlobal(self.QsL, self.Qs)

        # Set the corresponding thicknesses
        self.Qs.pointwiseDivide(self.Qs, self.areaGlobal)
        self.dm.globalToLocal(self.Qs, self.QsL)

        del rcID, tmp, data
        gc.collect()

        if MPIrank == 0 and self.verbose:
            print(
                "Move River Sediment Downstream (%0.02f seconds)"
                % (process_time() - t0),
                flush=True,
            )

        return

    def _hillSlope(self):
        r"""
        This function computes hillslope using a linear diffusion law commonly referred to as **soil creep**:

        .. math::
          \frac{\partial z}{\partial t}= \kappa_{D} \nabla^2 z

        in which :math:`\kappa_{D}` is the diffusion coefficient and can be defined with different values for the marine and land environments (set with `hillslopeKa` and `hillslopeKm` in the YAML input file).

        .. note::
            The hillslope processes in `gospl` are considered to be happening at the same rate for coarse and fine sediment sizes.

        """

        if self.Cda == 0.0 and self.Cdm == 0.0:
            return

        t0 = process_time()

        # Diffusion matrix construction
        Cd = np.full(self.lpoints, self.Cda, dtype=np.float64)
        Cd[self.seaID] = self.Cdm

        diffCoeffs = sethillslopecoeff(self.lpoints, Cd * self.dt)
        self.Diff = self._matrix_build_diag(diffCoeffs[:, 0])
        indptr = np.arange(0, self.lpoints + 1, dtype=petsc4py.PETSc.IntType)

        for k in range(0, self.maxnb):
            tmpMat = self._matrix_build()
            indices = self.FVmesh_ngbID[:, k].copy()
            data = diffCoeffs[:, k + 1]
            ids = np.nonzero(data == 0.0)
            indices[ids] = ids
            tmpMat.assemblyBegin()
            tmpMat.setValuesLocalCSR(
                indptr, indices.astype(petsc4py.PETSc.IntType), data,
            )
            tmpMat.assemblyEnd()
            self.Diff += tmpMat
            tmpMat.destroy()
        del ids, indices, indptr, diffCoeffs, Cd
        gc.collect()

        # Get elevation values for considered time step
        self.hGlobal.copy(result=self.hOld)
        self._solve_KSP(True, self.Diff, self.hOld, self.hGlobal)

        # Update cumulative erosion/deposition and elevation
        self.tmp.waxpy(-1.0, self.hOld, self.hGlobal)
        self.cumED.axpy(1.0, self.tmp)
        self.dm.globalToLocal(self.cumED, self.cumEDLocal)
        self.dm.globalToLocal(self.hGlobal, self.hLocal)

        if self.stratNb > 0:
            self.erodeStrat()
            if self.stratW is not None:
                self._deposeStrat(3)
            else:
                self._deposeStrat(0)

        if MPIrank == 0 and self.verbose:
            print(
                "Compute Hillslope Processes (%0.02f seconds)" % (process_time() - t0),
                flush=True,
            )

        return

    def _deposeStrat(self, stype):
        """
        Add deposition on top of an existing stratigraphic layer. The following variables will be recorded:

        - thickness of each stratigrapic layer `stratH` accounting for both erosion & deposition events.
        - proportion of fine sediment `stratF` contains in each stratigraphic layer.
        - proportion of weathered sediment `stratW` contains in each stratigraphic layer.
        - porosity of coarse sediment `phiS` in each stratigraphic layer computed at center of each layer.
        - porosity of fine sediment `phiF` in each stratigraphic layer computed at center of each layer.
        - porosity of weathered sediment `phiW` in each stratigraphic layer computed at center of each layer.
        - proportion of carbonate sediment `stratC` contains in each stratigraphic layer if the carbonate module is turned on.
        - porosity of carbonate sediment `phiC` in each stratigraphic layer computed at center of each layer when the carbonate module is turned on.

        :arg stype: sediment type (integer)
        """

        self.dm.globalToLocal(self.tmp, self.tmpL)
        depo = self.tmpL.getArray().copy()
        depo[depo < 1.0e-4] = 0.0
        if self.stratF is not None:
            fineH = self.stratH[:, self.stratStep] * self.stratF[:, self.stratStep]
        if self.stratW is not None:
            clayH = self.stratH[:, self.stratStep] * self.stratW[:, self.stratStep]
        if self.carbOn:
            carbH = self.stratH[:, self.stratStep] * self.stratC[:, self.stratStep]
        self.stratH[:, self.stratStep] += depo
        ids = np.where(depo > 0)[0]

        if stype == 0:
            self.phiS[ids, self.stratStep] = self.phi0s
        elif stype == 1:
            fineH[ids] += depo[ids]
            self.phiF[ids, self.stratStep] = self.phi0f
        elif stype == 2:
            carbH[ids] += depo[ids]
            self.phiC[ids, self.stratStep] = self.phi0c
        elif stype == 3:
            clayH[ids] += depo[ids]
            self.phiW[ids, self.stratStep] = self.phi0w

        if self.stratF is not None:
            self.stratF[ids, self.stratStep] = (
                fineH[ids] / self.stratH[ids, self.stratStep]
            )
            del fineH
        if self.stratW is not None:
            self.stratW[ids, self.stratStep] = (
                clayH[ids] / self.stratH[ids, self.stratStep]
            )
            del clayH
        if self.carbOn:
            self.stratC[ids, self.stratStep] = (
                carbH[ids] / self.stratH[ids, self.stratStep]
            )
            del carbH

        # Cleaning arrays
        del depo, ids
        gc.collect()

        return

    def erodeStrat(self):
        """
        This function removes eroded sediment thicknesses from the stratigraphic pile. The function takes into account the porosity values of considered lithologies in each eroded stratigraphic layers.

        It follows the following assumptions:

        - Eroded thicknesses from stream power law and hillslope diffusion are considered to encompass both the solid and void phase.
        - Only the solid phase will be moved dowstream by surface processes.
        - The corresponding deposit thicknesses for those freshly eroded sediments correspond to uncompacted thicknesses based on the porosity at surface given from the input file.
        """

        self.dm.globalToLocal(self.tmp, self.tmpL)
        ero = self.tmpL.getArray().copy()
        ero[ero > 0] = 0.0

        # Nodes experiencing erosion
        nids = np.where(ero < 0)[0]
        if len(nids) == 0:
            del ero, nids
            gc.collect()
            return

        # Cumulative thickness for each node
        self.stratH[nids, 0] += 1.0e6
        cumThick = np.cumsum(self.stratH[nids, self.stratStep :: -1], axis=1)[:, ::-1]
        boolMask = cumThick < -ero[nids].reshape((len(nids), 1))
        mask = boolMask.astype(int)

        if self.stratF is not None:
            # Get fine sediment eroded from river incision
            thickF = (
                self.stratH[nids, 0 : self.stratStep + 1]
                * self.stratF[nids, 0 : self.stratStep + 1]
            )
            # From fine thickness extract the solid phase that is eroded
            thFine = thickF * (1.0 - self.phiF[nids, 0 : self.stratStep + 1])
            thFine = np.sum((thFine * mask), axis=1)

        if self.stratW is not None:
            # Get weathered sediment eroded from river incision
            thickW = (
                self.stratH[nids, 0 : self.stratStep + 1]
                * self.stratW[nids, 0 : self.stratStep + 1]
            )
            # From weathered thickness extract the solid phase that is eroded
            thClay = thickW * (1.0 - self.phiW[nids, 0 : self.stratStep + 1])
            thClay = np.sum((thClay * mask), axis=1)

        # Get carbonate sediment eroded from river incision
        if self.carbOn:
            thickC = (
                self.stratH[nids, 0 : self.stratStep + 1]
                * self.stratC[nids, 0 : self.stratStep + 1]
            )
            # From carbonate thickness extract the solid phase that is eroded
            thCarb = thickC * (1.0 - self.phiC[nids, 0 : self.stratStep + 1])
            thCarb = np.sum((thCarb * mask), axis=1)
            # From sand thickness extract the solid phase that is eroded
            thickS = (
                self.stratH[nids, 0 : self.stratStep + 1] - thickF - thickC - thickW
            )
            thCoarse = thickS * (1.0 - self.phiS[nids, 0 : self.stratStep + 1])
            thCoarse = np.sum((thCoarse * mask), axis=1)
        else:
            # From sand thickness extract the solid phase that is eroded
            if self.stratF is not None:
                thickS = self.stratH[nids, 0 : self.stratStep + 1] - thickF - thickW
            else:
                thickS = self.stratH[nids, 0 : self.stratStep + 1]
            thCoarse = thickS * (1.0 - self.phiS[nids, 0 : self.stratStep + 1])
            thCoarse = np.sum((thCoarse * mask), axis=1)

        # Clear all stratigraphy points which are eroded
        cumThick[boolMask] = 0.0
        tmp = self.stratH[nids, : self.stratStep + 1]
        tmp[boolMask] = 0
        self.stratH[nids, : self.stratStep + 1] = tmp

        # Erode remaining stratal layers
        # Get non-zero top layer number
        eroLayNb = np.bincount(np.nonzero(cumThick)[0]) - 1
        eroVal = cumThick[np.arange(len(nids)), eroLayNb] + ero[nids]

        if self.stratF is not None:
            # Get thickness of each sediment type eroded in the remaining layer
            self.thFine = np.zeros(self.lpoints)
            # From fine thickness extract the solid phase that is eroded from this last layer
            tmp = (self.stratH[nids, eroLayNb] - eroVal) * self.stratF[nids, eroLayNb]
            tmp[tmp < 1.0e-8] = 0.0
            thFine += tmp * (1.0 - self.phiF[nids, eroLayNb])
            # Define the uncompacted fine thickness that will be deposited dowstream
            self.thFine[nids] = thFine / (1.0 - self.phi0f)
            self.thFine[self.thFine < 0.0] = 0.0

        if self.stratW is not None:
            # Get thickness of each sediment type eroded in the remaining layer
            self.thClay = np.zeros(self.lpoints)
            # From weathered thickness extract the solid phase that is eroded from this last layer
            tmp = (self.stratH[nids, eroLayNb] - eroVal) * self.stratW[nids, eroLayNb]
            tmp[tmp < 1.0e-8] = 0.0
            thClay += tmp * (1.0 - self.phiW[nids, eroLayNb])
            # Define the uncompacted weathered thickness that will be deposited dowstream
            self.thClay[nids] = thClay / (1.0 - self.phi0w)
            self.thClay[self.thClay < 0.0] = 0.0

        self.thCoarse = np.zeros(self.lpoints)
        if self.carbOn:
            # From carb thickness extract the solid phase that is eroded from this last layer
            self.thCarb = np.zeros(self.lpoints)
            tmp = (self.stratH[nids, eroLayNb] - eroVal) * self.stratC[nids, eroLayNb]
            tmp[tmp < 1.0e-8] = 0.0
            thCarb += tmp * (1.0 - self.phiC[nids, eroLayNb])
            # Define the uncompacted carbonate thickness that will be deposited dowstream
            self.thCarb[nids] = thCarb / (1.0 - self.phi0c)
            self.thCarb[self.thCarb < 0.0] = 0.0
            # From sand thickness extract the solid phase that is eroded from this last layer
            tmp = self.stratH[nids, eroLayNb] - eroVal
            tmp *= (
                1.0
                - self.stratC[nids, eroLayNb]
                - self.stratW[nids, eroLayNb]
                - self.stratF[nids, eroLayNb]
            )
            # Define the uncompacted sand thickness that will be deposited dowstream
            thCoarse += tmp * (1.0 - self.phiS[nids, eroLayNb])
            self.thCoarse[nids] = thCoarse / (1.0 - self.phi0s)
            self.thCoarse[self.thCoarse < 0.0] = 0.0
        else:
            # From sand thickness extract the solid phase that is eroded from this last layer
            tmp = self.stratH[nids, eroLayNb] - eroVal
            if self.stratF is not None:
                tmp *= 1.0 - self.stratF[nids, eroLayNb] - self.stratW[nids, eroLayNb]
            tmp[tmp < 1.0e-8] = 0.0
            # Define the uncompacted sand thickness that will be deposited dowstream
            thCoarse += tmp * (1.0 - self.phiS[nids, eroLayNb])
            self.thCoarse[nids] = thCoarse / (1.0 - self.phi0s)
            self.thCoarse[self.thCoarse < 0.0] = 0.0

        # Update thickness of top stratigraphic layer
        self.stratH[nids, eroLayNb] = eroVal
        self.stratH[nids, 0] -= 1.0e6
        self.stratH[self.stratH <= 0] = 0.0
        self.phiS[self.stratH <= 0] = 0.0
        if self.stratF is not None:
            self.stratF[self.stratH <= 0] = 0.0
            self.phiF[self.stratH <= 0] = 0.0
        if self.stratW is not None:
            self.stratW[self.stratH <= 0] = 0.0
            self.phiW[self.stratH <= 0] = 0.0
        if self.carbOn:
            self.stratC[self.stratH <= 0] = 0.0
            self.phiC[self.stratH <= 0] = 0.0

        self.thCoarse /= self.dt
        if self.stratF is not None:
            self.thFine /= self.dt
            del thickF, thFine
        if self.stratW is not None:
            self.thClay /= self.dt
            del thickW, thClay
        if self.carbOn:
            self.thCarb /= self.dt
            del thickC, thCarb

        del ero, nids, cumThick, boolMask, mask, tmp, eroLayNb, eroVal
        del thickS, thCoarse

        gc.collect()

        return

    def _elevStrat(self):
        """
        This function updates the current stratigraphic layer elevation.
        """

        self.stratZ[:, self.stratStep] = self.hLocal.getArray()

        return

    def _depthPorosity(self, depth):
        """
        This function uses the depth-porosity relationships to compute the porosities for each lithology and then the solid phase to get each layer thickness changes due to compaction.

        .. note::

            We assume that porosity cannot increase after unloading.

        :arg depth: depth below basement for each sedimentary layer

        :return: newH updated sedimentary layer thicknesses after compaction
        """

        # Depth-porosity functions
        phiS = self.phi0s * np.exp(depth / self.z0s)
        phiS = np.minimum(phiS, self.phiS[:, : self.stratStep + 1])
        if self.stratF is not None:
            phiF = self.phi0f * np.exp(depth / self.z0f)
            phiF = np.minimum(phiF, self.phiF[:, : self.stratStep + 1])
            phiW = self.phi0w * np.exp(depth / self.z0w)
            phiW = np.minimum(phiW, self.phiW[:, : self.stratStep + 1])
        if self.carbOn:
            phiC = self.phi0c * np.exp(depth / self.z0c)
            phiC = np.minimum(phiC, self.phiC[:, : self.stratStep + 1])

        # Compute the solid phase in each layers
        if self.stratF is not None:
            tmpF = (
                self.stratH[:, : self.stratStep + 1]
                * self.stratF[:, : self.stratStep + 1]
            )
            tmpF *= 1.0 - self.phiF[:, : self.stratStep + 1]
            tmpW = (
                self.stratH[:, : self.stratStep + 1]
                * self.stratW[:, : self.stratStep + 1]
            )
            tmpW *= 1.0 - self.phiW[:, : self.stratStep + 1]

        if self.carbOn:
            tmpC = (
                self.stratH[:, : self.stratStep + 1]
                * self.stratC[:, : self.stratStep + 1]
            )
            tmpC *= 1.0 - self.phiC[:, : self.stratStep + 1]
            tmpS = (
                self.stratC[:, : self.stratStep + 1]
                + self.stratF[:, : self.stratStep + 1]
                + self.stratW[:, : self.stratStep + 1]
            )
            tmpS = self.stratH[:, : self.stratStep + 1] * (1.0 - tmpS)
            tmpS *= 1.0 - self.phiS[:, : self.stratStep + 1]
            solidPhase = tmpC + tmpS + tmpF + tmpW
        else:
            if self.stratF is not None:
                tmpS = self.stratH[:, : self.stratStep + 1] * (
                    1.0
                    - self.stratF[:, : self.stratStep + 1]
                    - self.stratW[:, : self.stratStep + 1]
                )
                tmpS *= 1.0 - self.phiS[:, : self.stratStep + 1]
                solidPhase = tmpS + tmpF + tmpW
            else:
                tmpS = self.stratH[:, : self.stratStep + 1]
                tmpS *= 1.0 - self.phiS[:, : self.stratStep + 1]
                solidPhase = tmpS

        # Get new layer thickness after porosity change
        if self.stratF is not None:
            tmpF = self.stratF[:, : self.stratStep + 1] * (
                1.0 - phiF[:, : self.stratStep + 1]
            )
            tmpW = self.stratW[:, : self.stratStep + 1] * (
                1.0 - phiW[:, : self.stratStep + 1]
            )
        if self.carbOn:
            tmpC = self.stratC[:, : self.stratStep + 1] * (
                1.0 - phiC[:, : self.stratStep + 1]
            )
            tmpS = (
                1.0
                - self.stratF[:, : self.stratStep + 1]
                - self.stratC[:, : self.stratStep + 1]
                - self.stratW[:, : self.stratStep + 1]
            )
            tmpS *= 1.0 - phiS[:, : self.stratStep + 1]
            tot = tmpS + tmpC + tmpF + tmpW
        else:
            if self.stratF is not None:
                tmpS = (
                    1.0
                    - self.stratF[:, : self.stratStep + 1]
                    - self.stratW[:, : self.stratStep + 1]
                ) * (1.0 - phiS[:, : self.stratStep + 1])
                tot = tmpS + tmpF + tmpW
            else:
                tot = 1.0 - phiS[:, : self.stratStep + 1]

        ids = np.where(tot > 0.0)
        newH = np.zeros(tot.shape)
        newH[ids] = solidPhase[ids] / tot[ids]
        newH[newH <= 0] = 0.0
        phiS[newH <= 0] = 0.0
        if self.stratF is not None:
            phiF[newH <= 0] = 0.0
            phiW[newH <= 0] = 0.0
        if self.carbOn:
            phiC[newH <= 0] = 0.0

        # Update porosities in each sedimentary layer
        self.phiS[:, : self.stratStep + 1] = phiS
        if self.stratF is not None:
            self.phiF[:, : self.stratStep + 1] = phiF
            self.phiW[:, : self.stratStep + 1] = phiW
        if self.carbOn:
            self.phiC[:, : self.stratStep + 1] = phiC

        del phiS, solidPhase
        del ids, tmpS, tot
        if self.stratF is not None:
            del tmpF, phiF, tmpW, phiW
        if self.carbOn:
            del phiC, tmpC

        gc.collect()

        return newH

    def getCompaction(self):
        """
        This function computes the changes in sedimentary layers porosity and thicknesses due to compaction.

        .. note::

            We assume simple depth-porosiy relationships for each sediment type available in each layers.
        """

        t0 = process_time()
        topZ = np.vstack(self.hLocal.getArray())
        totH = np.sum(self.stratH[:, : self.stratStep + 1], axis=1)

        # Height of the sediment column above the center of each layer is given by
        cumZ = -np.cumsum(self.stratH[:, self.stratStep :: -1], axis=1) + topZ
        elev = np.append(topZ, cumZ[:, :-1], axis=1)
        zlay = np.fliplr(elev - np.fliplr(self.stratH[:, : self.stratStep + 1] / 2.0))

        # Compute lithologies porosities for each depositional layers
        # Get depth below basement
        depth = zlay - topZ

        # Now using depth-porosity relationships we compute the porosities
        newH = self._depthPorosity(depth)

        # Get the total thickness changes induced by compaction and
        # update the elevation accordingly
        dz = totH - np.sum(newH, axis=1)
        dz[dz <= 0] = 0.0
        self.hLocal.setArray(topZ.flatten() - dz.flatten())
        self.dm.localToGlobal(self.hLocal, self.hGlobal)

        # Update each layer thicknesses
        self.stratH[:, : self.stratStep + 1] = newH
        del dz, newH, totH, topZ
        del depth, zlay, cumZ, elev

        gc.collect()

        if MPIrank == 0 and self.verbose:
            print(
                "Compute Lithology Porosity Values (%0.02f seconds)"
                % (process_time() - t0),
                flush=True,
            )

        return
