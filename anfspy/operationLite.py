import random

# from .lp_solve import LinearProgram
# from .lp_solve import Row


class OperationLite():
    def __init__(self):
        """
        @param planningHorizon: the planning horizon
        @type planningHorizon: L{int}
        @param storagePenalty: the storage opportuntiy designCost
        @type storagePenalty: L{float}
        @param islPenalty: the ISL opportuntiy designCost
        @type islPenalty: L{float}
        """
        pass
        # self.masterStream = random.Random(self.seed)
        # self.shuffleStream = random.Random(self.masterStream.random())
        # self.orderStream = random.Random(self.masterStream.random())

    def execute(self, context):
        """
        Executes this operations model.
        @param controller: the controller for this operations model
        @type controller: L{Entity}
        @param context: the context of operations
        @type context: L{Context}
        """
        pass

        #             if all(lp.get(R_c[0][i][j]) < 1        federates = context.federates
        # random.shuffle(federates, random=self.orderStream.random)
        #
        # federates = context.federates
        # for f in federates:
        #     f.time = context.time
        #
        #
        #
        #
        # minTime = context.time
        # maxTime = (context.time + self.planningHorizon
        #            if context.maxTime is None else
        #            min(context.maxTime, context.time + self.planningHorizon))
        #
        # with LinearProgram(name='OFS LP for {}'.format(controller.name)) as lp:
        #     S = []  # S[i][j]: satellite i senses demand j
        #     E_d = []  # E_d[t][i][j]: at time t satellite i holds data for demand j
        #     E_c0 = []  # E_c0[i][j]: satellite i initially holds data for contract j
        #     E_c = []  # E_c[t][i][j]: at time t satellite i holds data for contract j
        #     T_d = []  # T_d[t][i][j][k][l]: at time t transmit data from satellite i to ground station j using protocol k for demand l
        #     T_c = []  # T_c[t][i][j][k][l]: at time t transmit data from satellite i to ground station j using protocol k for contract l
        #     L_d = []  # L_d[t][i][j][k][l]: at time t transmit data from isl satellite i to isl satellite j using protocol k for demand l
        #     L_c = []  # L_c[t][i][j][k][l]: at time t transmit data from isl satellite i to isl satellite j using protocol k for contract l
        #     R_d = []  # R_d[t][i][j]: at time t resolve data in system i for demand j
        #     R_c = []  # R_c[t][i][j]: at time t resolve data in system i for contract j
        #     J = Row()  # objective function
        #
        #     demands = [e for e in context.currentEvents if e.isDemand()]
        #     elements = controller.getElements()
        #     federates = controller.getFederates()
        #     satellites = [e for e in elements if e.isSpace()]
        #     satellitesISL = [e for e in satellites
        #                      if any(m.isTransceiver() and m.isISL() for m in e.modules)]
        #     stations = [e for e in elements if e.isGround()]
        #     contracts = controller.getContracts()
        #
        #     protocolsSGL = list(set([m.protocol for e in elements
        #                              for m in e.modules if m.isTransceiver() and m.isSGL()]))
        #     protocolsISL = list(set([m.protocol for e in elements
        #                              for m in e.modules if m.isTransceiver() and m.isISL()]))
        #     phenomena = ['VIS', 'SAR', None]
        #
        #     for i, satellite in enumerate(satellites):
        #         S.insert(i, [])
        #         for j, demand in enumerate(demands):
        #             # satellite i senses data for demand j
        #             S[i].insert(j, lp.addColumn('{}-S-{}'.format(
        #                 satellite.name, demand.name), isBinary=True))
        #             # constrain sensing per satellite
        #             lp.addConstraint(Row().add(S[i][j], 1), 'LE',
        #                              1 if satellite.canSense(demand) else 0,
        #                              '{} can sense {}'.format(satellite.name,
        #                                                       demand.name))
        #         for phenomenon in phenomena:
        #             r = Row()
        #             for j, demand in enumerate(demands):
        #                 if phenomenon is None or demand.phenomenon == phenomenon:
        #                     r.add(S[i][j], demand.size)
        #             # constrain maximum data sensed by satellite
        #             lp.addConstraint(r, 'LE',
        #                              min(satellite.getMaxSensed(phenomenon)
        #                                  - satellite.getSensed(phenomenon),
        #                                  satellite.getMaxStored(phenomenon)
        #                                  - satellite.getStored(phenomenon)),
        #                              '{} max sense {}'.format(satellite.name,
        #                                                       phenomenon))
        #         # set initial data stored
        #         E_c0.insert(i, [])
        #         for j, contract in enumerate(contracts):
        #             E_c0[i].insert(j, 1 if any(d.contract is contract
        #                                        for m in satellite.modules
        #                                        for d in m.data) else 0)
        #
        #     for j, demand in enumerate(demands):
        #         r = Row()
        #         for i, satellite in enumerate(satellites):
        #             r.add(S[i][j], 1)
        #         lp.addConstraint(r, 'LE', 1, '{} max sensed'.format(demand.name))
        #
        #     for t, time in enumerate(range(minTime, maxTime + 1)):
        #         E_d.insert(t, [])
        #         E_c.insert(t, [])
        #         for i, satellite in enumerate(satellites):
        #             E_d[t].insert(i, [])
        #             E_c[t].insert(i, [])
        #             for j, demand in enumerate(demands):
        #                 # satellite i stores data for new contract j
        #                 E_d[t][i].insert(j, lp.addColumn('{}-E-{}@{}'.format(
        #                     satellite.name, demand.name, time), isBinary=True))
        #                 # penalty for opportunity designCost
        #                 J.add(E_d[t][i][j], demand.size * (self.storagePenalty
        #                                                    if self.storagePenalty is not None
        #                                                    else self.getStoragePenalty(satellite, context)))
        #             for j, contract in enumerate(contracts):
        #                 # satellite i stores data for contract j
        #                 E_c[t][i].insert(j, lp.addColumn('{}-E-{}@{}'.format(
        #                     satellite.name, contract.name, time), isBinary=True))
        #                 # penalty for opportunity designCost
        #                 J.add(E_c[t][i][j], contract.demand.size * (self.storagePenalty
        #                                                             if self.storagePenalty is not None
        #                                                             else self.getStoragePenalty(satellite, context)))
        #             for phenomenon in phenomena:
        #                 r = Row()
        #                 for j, demand in enumerate(demands):
        #                     if phenomenon is None or demand.phenomenon == phenomenon:
        #                         r.add(E_d[t][i][j], demand.size)
        #                 for j, contract in enumerate(contracts):
        #                     if phenomenon is None or contract.demand.phenomenon == phenomenon:
        #                         r.add(E_c[t][i][j], contract.demand.size)
        #                 # constrain data stored in satellite
        #                 lp.addConstraint(r, 'LE', satellite.getMaxStored(phenomenon),
        #                                  '{} max store {} at {}'.format(
        #                                      satellite.name, phenomenon, time))
        #         T_d.insert(t, [])
        #         T_c.insert(t, [])
        #         for i, satellite in enumerate(satellites):
        #             T_d[t].insert(i, [])
        #             T_c[t].insert(i, [])
        #             txLocation = context.propagate(satellite.location, time - context.time)
        #             for j, station in enumerate(stations):
        #                 T_d[t][i].insert(j, [])
        #                 T_c[t][i].insert(j, [])
        #                 rxLocation = context.propagate(station.location, time - context.time)
        #                 for k, protocol in enumerate(protocolsSGL):
        #                     T_d[t][i][j].insert(k, [])
        #                     T_c[t][i][j].insert(k, [])
        #                     r = Row()
        #                     maxSize = 0
        #                     for l, demand in enumerate(demands):
        #                         T_d[t][i][j][k].insert(l, lp.addColumn(
        #                             '{}-T({}/{})-{}@{}'.format(
        #                                 satellite.name, demand.name,
        #                                 protocol, station.name, time),
        #                             isBinary=True))
        #                         r.add(T_d[t][i][j][k][l], demand.size)
        #                         maxSize = max(maxSize, demand.size
        #                         if controller.couldTransport(
        #                             protocol, demand.generateData(),
        #                             satellite, station,
        #                             txLocation, rxLocation, context)
        #                            and not demand.isDefaultedAt(
        #                             time - context.time)
        #                         else 0)
        #                     for l, contract in enumerate(contracts):
        #                         T_c[t][i][j][k].insert(l, lp.addColumn(
        #                             '{}-T({}/{})-{}@{}'.format(
        #                                 satellite.name, contract.name,
        #                                 protocol, station.name, time),
        #                             isBinary=True))
        #                         r.add(T_c[t][i][j][k][l], contract.demand.size)
        #                         maxSize = max(maxSize, contract.demand.size
        #                         if controller.couldTransport(
        #                             protocol, contract.demand.generateData(),
        #                             satellite, station,
        #                             txLocation, rxLocation, context)
        #                            and not contract.demand.isDefaultedAt(
        #                             contract.elapsedTime + time - context.time)
        #                         else 0)
        #                     # constrain transmission by visibility
        #                     lp.addConstraint(r, 'LE', maxSize, '{}-{} visibility {} at {}'
        #                                      .format(satellite.name, station.name, protocol, time))
        #         for i, satellite in enumerate(satellites):
        #             for k, protocol in enumerate(protocolsSGL):
        #                 r = Row()
        #                 for j, station in enumerate(stations):
        #                     for l, demand in enumerate(demands):
        #                         r.add(T_d[t][i][j][k][l], demand.size)
        #                     for l, contract in enumerate(contracts):
        #                         r.add(T_c[t][i][j][k][l], contract.demand.size)
        #                 # constrain data transmitted by satellite
        #                 lp.addConstraint(r, 'LE', satellite.getMaxTransmitted(protocol)
        #                                  - (satellite.getTransmitted(protocol)
        #                                     if time == minTime else 0),
        #                                  '{} max transmit {} at {}'
        #                                  .format(satellite.name, protocol, time))
        #         for j, station in enumerate(stations):
        #             for k, protocol in enumerate(protocolsSGL):
        #                 r = Row()
        #                 for i, satellite in enumerate(satellites):
        #                     for l, demand in enumerate(demands):
        #                         r.add(T_d[t][i][j][k][l], demand.size)
        #                     for l, contract in enumerate(contracts):
        #                         r.add(T_c[t][i][j][k][l], contract.demand.size)
        #                 # constrain data received by station
        #                 lp.addConstraint(r, 'LE', station.getMaxReceived(protocol)
        #                                  - (station.getReceived(protocol)
        #                                     if time == minTime else 0),
        #                                  '{} max receive {} at {}'
        #                                  .format(station.name, protocol, time))
        #         L_d.insert(t, [])
        #         L_c.insert(t, [])
        #         for i, txSatellite in enumerate(satellitesISL):
        #             L_d[t].insert(i, [])
        #             L_c[t].insert(i, [])
        #             txLocation = context.propagate(txSatellite.location, time - context.time)
        #             for j, rxSatellite in enumerate(satellitesISL):
        #                 L_d[t][i].insert(j, [])
        #                 L_c[t][i].insert(j, [])
        #                 rxLocation = context.propagate(rxSatellite.location, time - context.time)
        #                 for k, protocol in enumerate(protocolsISL):
        #                     L_d[t][i][j].insert(k, [])
        #                     L_c[t][i][j].insert(k, [])
        #                     r = Row()
        #                     maxSize = 0
        #                     for l, demand in enumerate(demands):
        #                         L_d[t][i][j][k].insert(l, lp.addColumn(
        #                             '{}-T({}/{})-{}@{}'.format(
        #                                 txSatellite.name, demand.name,
        #                                 protocol, rxSatellite.name, time),
        #                             isBinary=True))
        #                         # small penalty for opportunity designCost
        #                         J.add(L_d[t][i][j][k][l], self.islPenalty * demand.size)
        #                         r.add(L_d[t][i][j][k][l], demand.size)
        #                         maxSize = max(maxSize, demand.size
        #                         if controller.couldTransport(
        #                             protocol, demand.generateData(),
        #                             txSatellite, rxSatellite,
        #                             txLocation, rxLocation, context)
        #                            and not demand.isDefaultedAt(
        #                             time - context.time)
        #                         else 0)
        #                     for l, contract in enumerate(contracts):
        #                         L_c[t][i][j][k].insert(l, lp.addColumn(
        #                             '{}-T({}/{})-{}@{}'.format(
        #                                 txSatellite.name, contract.name,
        #                                 protocol, rxSatellite.name, time),
        #                             isBinary=True))
        #                         # small penalty for opportunity designCost
        #                         J.add(L_c[t][i][j][k][l], self.islPenalty * contract.demand.size)
        #                         r.add(L_c[t][i][j][k][l], contract.demand.size)
        #                         maxSize = max(maxSize, contract.demand.size
        #                         if controller.couldTransport(
        #                             protocol, contract.demand.generateData(),
        #                             txSatellite, rxSatellite,
        #                             txLocation, rxLocation, context)
        #                            and not contract.demand.isDefaultedAt(
        #                             contract.elapsedTime + time - context.time)
        #                         else 0)
        #                     # constrain transmission by visibility
        #                     lp.addConstraint(r, 'LE', maxSize, '{}-{} visibility {} at {}'
        #                                      .format(txSatellite.name, rxSatellite.name,
        #                                              protocol, time))
        #         for i, txSatellite in enumerate(satellitesISL):
        #             for k, protocol in enumerate(protocolsISL):
        #                 r = Row()
        #                 for j, rxSatellite in enumerate(satellitesISL):
        #                     for l, demand in enumerate(demands):
        #                         r.add(L_d[t][i][j][k][l], demand.size)
        #                     for l, contract in enumerate(contracts):
        #                         r.add(L_c[t][i][j][k][l], contract.demand.size)
        #                 # constrain data transmitted by satellite
        #                 lp.addConstraint(r, 'LE', txSatellite.getMaxTransmitted(protocol)
        #                                  - (txSatellite.getTransmitted(protocol)
        #                                     if time == minTime else 0),
        #                                  '{} max transmit {} at {}'
        #                                  .format(txSatellite.name, protocol, time))
        #         for j, rxSatellite in enumerate(satellitesISL):
        #             for k, protocol in enumerate(protocolsISL):
        #                 r = Row()
        #                 for i, txSatellite in enumerate(satellitesISL):
        #                     for l, demand in enumerate(demands):
        #                         r.add(L_d[t][i][j][k][l], demand.size)
        #                     for l, contract in enumerate(contracts):
        #                         r.add(L_c[t][i][j][k][l], contract.demand.size)
        #                 # constrain data received by station
        #                 lp.addConstraint(r, 'LE', rxSatellite.getMaxReceived(protocol)
        #                                  - (rxSatellite.getReceived(protocol)
        #                                     if time == minTime else 0),
        #                                  '{} max receive {} at {}'
        #                                  .format(rxSatellite.name, protocol, time))
        #         R_d.insert(t, [])
        #         R_c.insert(t, [])
        #         for i, element in enumerate(elements):
        #             location = context.propagate(element.location, time - context.time)
        #             R_d[t].insert(i, [])
        #             R_c[t].insert(i, [])
        #             for j, demand in enumerate(demands):
        #                 R_d[t][i].insert(j, lp.addColumn('{}-R-{}@{}'.format(
        #                     element.name, demand.name, time), isBinary=True))
        #                 J.add(R_d[t][i][j], demand.getValueAt(time - context.time)
        #                 if demand.isCompletedAt(location)
        #                 else demand.getDefaultValue())
        #             for j, contract in enumerate(contracts):
        #                 R_c[t][i].insert(j, lp.addColumn('{}-R-{}@{}'.format(
        #                     element.name, contract.name, time), isBinary=True))
        #                 J.add(R_c[t][i][j], contract.demand.getValueAt(
        #                     contract.elapsedTime + time - context.time)
        #                 if contract.demand.isCompletedAt(location)
        #                 else contract.demand.getDefaultValue())
        #         for i, satellite in enumerate(satellites):
        #             R_i = elements.index(satellite)
        #             for j, demand in enumerate(demands):
        #                 r = Row()
        #                 if time == minTime:
        #                     r.add(S[i][j], 1)
        #                 else:
        #                     r.add(E_d[t - 1][i][j], 1)
        #                 r.add(E_d[t][i][j], -1)
        #                 r.add(R_d[t][R_i][j], -1)
        #                 for k, station in enumerate(stations):
        #                     for l, protocol in enumerate(protocolsSGL):
        #                         r.add(T_d[t][i][k][l][j], -1)
        #                 if satellite in satellitesISL:
        #                     isl_i = satellitesISL.index(satellite)
        #                     for k, rxSatellite in enumerate(satellitesISL):
        #                         for l, protocol in enumerate(protocolsISL):
        #                             r.add(L_d[t][isl_i][k][l][j], -1)
        #                             r.add(L_d[t][k][isl_i][l][j], 1)
        #                 # constrain net flow of new contracts at each satellite
        #                 lp.addConstraint(r, 'EQ', 0, '{} net flow {} at {}'
        #                                  .format(satellite.name, demand.name, time))
        #             for j, contract in enumerate(contracts):
        #                 r = Row()
        #                 if time == minTime:
        #                     # existing contracts are initial conditions
        #                     pass
        #                 else:
        #                     r.add(E_c[t - 1][i][j], 1)
        #                 r.add(E_c[t][i][j], -1)
        #                 r.add(R_c[t][R_i][j], -1)
        #                 for k, station in enumerate(stations):
        #                     for l, protocol in enumerate(protocolsSGL):
        #                         r.add(T_c[t][i][k][l][j], -1)
        #                 if satellite in satellitesISL:
        #                     isl_i = satellitesISL.index(satellite)
        #                     for k, rxSatellite in enumerate(satellitesISL):
        #                         for l, protocol in enumerate(protocolsISL):
        #                             r.add(L_c[t][isl_i][k][l][j], -1)
        #                             r.add(L_c[t][k][isl_i][l][j], 1)
        #                 # constrain net flow of contracts at each satellite
        #                 lp.addConstraint(r, 'EQ', -1 * (E_c0[i][j] if time == minTime else 0),
        #                                  '{} net flow {} at {}'
        #                                  .format(satellite.name, contract.name, time))
        #         if time + 1 > maxTime and self.planningHorizon > 0:
        #             for i, satellite in enumerate(satellites):
        #                 r = Row()
        #                 for j, demand in enumerate(demands):
        #                     r.add(E_d[t][i][j], 1)
        #                 for j, contract in enumerate(contracts):
        #                     r.add(E_c[t][i][j], 1)
        #                 # constrain boundary flow of each satellite
        #                 lp.addConstraint(r, 'EQ', 0, '{} boundary flow'
        #                                  .format(satellite.name))
        #         for k, station in enumerate(stations):
        #             R_k = elements.index(station)
        #             for j, demand in enumerate(demands):
        #                 r = Row()
        #                 r.add(R_d[t][R_k][j], -1)
        #                 for i, satellite in enumerate(satellites):
        #                     for l, protocol in enumerate(protocolsSGL):
        #                         r.add(T_d[t][i][k][l][j], 1)
        #                 # constrain net flow of new contracts at each station
        #                 lp.addConstraint(r, 'EQ', 0, '{} net flow {} at {}'
        #                                  .format(station.name, demand.name, time))
        #             for j, contract in enumerate(contracts):
        #                 r = Row()
        #                 r.add(R_c[t][R_k][j], -1)
        #                 for i, satellite in enumerate(satellites):
        #                     for l, protocol in enumerate(protocolsSGL):
        #                         r.add(T_c[t][i][k][l][j], 1)
        #                 # constrain net flow of contracts at each station
        #                 lp.addConstraint(r, 'EQ', 0, '{} net flow {} at {}'
        #                                  .format(station.name, contract.name, time))
        #     for federate in federates:
        #         r = Row()
        #         for j, demand in enumerate(demands):
        #             if federate.canContract(demand, context):  # TODO does not consider priority
        #                 for i, element in enumerate(elements):
        #                     location = context.propagate(element.location, time - context.time)
        #                     r.add(R_d[0][i][j], (demand.getValueAt(0)
        #                                          if demand.isCompletedAt(location)
        #                                          else demand.getDefaultValue()))
        #         for j, contract in enumerate(contracts):
        #             if contract in federate.contracts:
        #                 for i, element in enumerate(elements):
        #                     location = context.propagate(element.location, time - context.time)
        #                     r.add(R_c[0][i][j], (contract.demand.getValueAt(contract.elapsedTime)
        #                                          if contract.demand.isCompletedAt(location)
        #                                          else contract.demand.getDefaultValue()))
        #         lp.addConstraint(r, 'GE', -1 - federate.cash,
        #                          '{} net cash must be positive'
        #                          .format(federate.name))
        #
        #     lp.setObjective(J, False)
        #     code, description = lp.solve()
        #
        #     if code > 1:
        #         logging.warning(description)
        #         with open('lp_debug.txt', 'w+') as f:
        #             f.write(lp.dumpProgram())
        #     else:
        #         """ debug code
        #         with open('lp_solution_{}_{}.txt'.format(
        #             controller.name, context.time), 'w+') as f:
        #             f.write(lp.dumpSolution())
        #         with open('lp_program_{}_{}.txt'.format(
        #             controller.name, context.time), 'w+') as f:
        #             f.write(lp.dumpProgram())
        #         """
        #
        #         def _transportContract(operations, satellite, contract, context):
        #             i = satellites.index(satellite)
        #             R_i = elements.index(satellite)
        #             j = contracts.index(contract)
        #             data = context.getData(contract)
        #             if data is not None:
        #                 if lp.get(R_c[0][R_i][j]) > 0:
        #                     controller.resolve(contract, context)
        #                 elif lp.get(E_c[0][i][j]) > 0:
        #                     satellite.store(data)
        #                 elif any(any(lp.get(T_c[0][i][k][l][j])
        #                              for k, station in enumerate(stations))
        #                          for l, protocol in enumerate(protocolsSGL)):
        #                     for k, station in enumerate(stations):
        #                         for l, protocol in enumerate(protocolsSGL):
        #                             if (lp.get(T_c[0][i][k][l][j])):
        #                                 controller.transport(protocol, data,
        #                                                      satellite, station, context)
        #                                 controller.resolve(contract, context)
        #                 elif satellite in satellitesISL:
        #                     isl_i = satellitesISL.index(satellite)
        #                     for k, rxSatellite in enumerate(satellitesISL):
        #                         for l, protocol in enumerate(protocolsISL):
        #                             if (lp.get(L_c[0][isl_i][k][l][j])):
        #                                 controller.transport(protocol, data,
        #                                                      satellite, rxSatellite, context)
        #                                 _transportContract(operations, rxSatellite,
        #                                                    contract, context)
        #
        #         def _transportDemand(operations, satellite, demand, context):
        #             i = satellites.index(satellite)
        #             R_i = elements.index(satellite)
        #             j = demands.index(demand)
        #             contract = context.getContract(demand)
        #             data = context.getData(contract)
        #             if contract is not None and data is not None:
        #                 if lp.get(R_d[0][R_i][j]) > 0:
        #                     controller.resolve(contract, context)
        #                 elif lp.get(E_d[0][i][j]) > 0:
        #                     satellite.store(data)
        #                 elif any(any(lp.get(T_d[0][i][k][l][j])
        #                              for k, station in enumerate(stations))
        #                          for l, protocol in enumerate(protocolsSGL)):
        #                     for k, station in enumerate(stations):
        #                         for l, protocol in enumerate(protocolsSGL):
        #                             if (lp.get(T_d[0][i][k][l][j])):
        #                                 controller.transport(protocol, data,
        #                                                      satellite, station, context)
        #                                 controller.resolve(contract, context)
        #                 elif satellite in satellitesISL:
        #                     isl_i = satellitesISL.index(satellite)
        #                     for k, rxSatellite in enumerate(satellitesISL):
        #                         for l, protocol in enumerate(protocolsISL):
        #                             if (lp.get(L_d[0][isl_i][k][l][j])):
        #                                 controller.transport(protocol, data,
        #                                                      satellite, rxSatellite, context)
        #                                 _transportDemand(operations, rxSatellite,
        #                                                  demand, context)
        #
        #         # first, transport contracts to resolution
        #         for j, contract in enumerate(contracts):
        #             if any(lp.get(R_c[0][i][j]) > 0
        #                    for i, element in enumerate(elements)):
        #                 logging.debug('Transporting contract {} for resolution...'
        #                               .format(contract.name))
        #                 satellite = context.getDataElement(contract)
        #                 _transportContract(self, satellite, contract, context)
        #
        #         # second, sense and transport demands to resolution
        #         for j, demand in enumerate(demands):
        #             if any(lp.get(R_d[0][i][j]) > 0
        #                    for i, element in enumerate(elements)):
        #                 logging.debug('Sensing and transporting demand {} for resolution...'
        #                               .format(demand.name))
        #                 satellite = next(e for i, e in enumerate(satellites)
        #                                  if lp.get(S[i][j]) > 0)
        #                 contract = controller.contract(demand, context)
        #                 controller.senseAndStore(contract, satellite, context)
        #                 _transportDemand(self, satellite, demand, context)
        #
        #         # third, sense all demands to be stored
        #         for j, demand in enumerate(demands):
        #             if (all(lp.get(R_d[0][i][j]) < 1
        #                     for i, element in enumerate(elements))
        #                 and any(lp.get(S[i][j]) > 0
        #                         for i, element in enumerate(satellites))):
        #                 logging.debug('Sensing demand {} for storage...'
        #                               .format(demand.name))
        #                 satellite = next(e for i, e in enumerate(satellites)
        #                                  if lp.get(S[i][j]) > 0)
        #                 contract = controller.contract(demand, context)
        #                 controller.senseAndStore(contract, satellite, context)
        #
        #         # fourth, transport demands to storage
        #         for j, demand in enumerate(demands):
        #             if (all(lp.get(R_d[0][i][j]) < 1
        #                     for i, element in enumerate(elements))
        #                 and any(lp.get(S[i][j]) > 0
        #                         for i, element in enumerate(satellites))):
        #                 logging.debug('Transporting demand {} for storage...'
        #                               .format(demand.name))
        #                 satellite = next(e for i, e in enumerate(satellites)
        #                                  if lp.get(S[i][j]) > 0)
        #                 _transportDemand(self, satellite, demand, context)
        #
        #         # finally, transport contracts to storage
        #         for j, contract in enumerate(contracts):
        #                    for i, element in enumerate(elements)):
        #                 logging.debug('Transporting contract {} for storage...'
        #                               .format(contract.name))
        #                 satellite = context.getDataElement(contract)
        #                 _transportContract(self, satellite, contract, context)