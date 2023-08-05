import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Poison(Distribution):
    """Posion distribution class

    Attributes:
        interval(float): a time period within which you observe the events
        events_per_time(float): the number of events that happen per time
        lambda(float): the rate paramter indicating the expected events in an interval

        calculate_pmf: calculating the prbability mass function of poisson distribution
        calulate_waiting_time: calculating the waiting time before an event happens

    """
    def __init__(self,interval,events_per_time):
       
        self.interval=interval
        self.events_per_time=events_per_time
        self.lambdas = interval * events_per_time
        Distribution.__init__(self,self.lambdas,self.lambdas)

    def calculate_pmf(self, k):
        """calculating the prbability mass function of poisson distribution

        Args:
            None

        Returns:
            pmf(float): the prbability mass function of poisson distribution
        """

        pmf=math.exp(-self.lambdas) * math.pow(self.lambdas, k)/math.factorial(k)

        return pmf

    def plot_bar_pmf(self):

        """ploting the probability mass function of the posion distribution

        Args:
            None
        
        Returns:
            x(list): a list of values denoting the number of events in an interval
            y(list): a list containing the probability corresponding to the series of values in x

        """

        x=list(range(2*self.lambdas+1))

        y=list(map(self.calculate_pmf,x))

        plt.bar(x=x,height=y)

        return (x,y)

    def calculate_waiting_time(self,t):
        """calculating the probability of waiting time being over a certain time

        Args:
            t(float): certain waiting time
        
        Returns:
            waiting_time_probability(float): the probability of waiting time being over a certain time
        """

        waiting_time_probability=math.exp(-self.events_per_time*t)

        return waiting_time_probability



