from CoolProp import CoolProp as CP

class State(object):
    """
        The state of a fluid is defined with two unique intensive properties
        this class keeps track of the state of the fluid and solves for all other 
        intensive properties. 
    """
    def __init__(self, fluid, **kwargs):
        """
        fluid: The type of fluid this is.
        flowRate: The mass flow rate of the stream, kg/s
        kwargs: intensive properties to define the state.
        The Properties that we are interested in are:
        h, specific Enthalpy
        u, specific Internal Energy
        v, specific Volume
        s, specific Entropy
        m, specific mass flow rate 
        """
        self.defined = False
        self.fluid = fluid
        self.properties = dict()
        if kwargs is not None:
            self.properties.update(kwargs)
        

    def define(self, **kwargs):
        """
        Define the fluid state based off of the inputed properties
        """
        #Make a list of defined properties
        inputProp = []
        if kwargs is not None:
            self.properties.update(kwargs)
        for key in self.properties.keys():
            inputProp.extend([key.capitalize(), self.properties[key]])
        inputProp.append(self.fluid)
        try:
            self.properties.update(
            T = CP.PropsSI('T', *inputProp),
            P = CP.PropsSI('P', *inputProp),
            h = CP.PropsSI('H', *inputProp),
            s = CP.PropsSI('S',*inputProp),
            u = CP.PropsSI('U', *inputProp),
            v = 1/CP.PropsSI('D', *inputProp))
            self.defined = True
        except Exception as ex:
            self.defined = False
            print ex
        return self.defined


    def exergy_f(self, t0, p0):
        deadState = State('Water', T=t0, P=p0)
        if deadState.define():
            self._exergy_f = ((self.properties['h'] - deadState.properties['h']) 
                            -t0*(self.properties['s']-deadState.properties['s']))
            return self._exergy_f
        else:
            return False
        
    def exergy(self, t0, p0):
        deadState = State('Water', T=t0, P=p0)
        if deadState.define():
            self._exergy = ((self.properties['u'] - deadState.properties['u']) 
                            +p0*(self.properties['v'] - deadState.properties['v'])
                            -t0*(self.properties['s']-deadState.properties['s']))
            return self._exergy
        else:
            return False
    def __add__(self, other):
        pass


    def isDefined(self):
        pass
    