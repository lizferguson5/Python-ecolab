import unittest
import agents
import environment
import numpy
import ecolab
from scipy.io import loadmat

class EnvironmentTests(unittest.TestCase):
    #Tests that a 5 x 5 environment is created as we expect it to be

    def setUp(self):
        self.env = environment.environment(5)

    def testBMSize(self):
        self.failUnless(self.env.bm_size==5)

class MATLABTest1(unittest.TestCase):
    #Compares our results with the original MATLAB ecolab that was run with 
    #ecolab(5,30,2,100) 
    #and rng(1)

    def setUp(self):
        numpy.random.seed(1)
        self.env = environment.environment(10) #Create a 5 x 5 environment
        (self.rabbits,self.foxes) = ecolab.create_agents(30,2,self.env)

    def testRabbit1(self):
        #Ensures that the first rabbit in the rabbits list has the same properties 
        #as the MATLAB model
        self.failUnlessAlmostEqual(self.rabbits[0].pos[0] ,4.7532, places=4)
        self.failUnlessAlmostEqual(self.rabbits[0].pos[1] ,1.8851, places=4)
        self.failUnlessEqual(self.rabbits[0].age,1)  
        self.failUnlessEqual(self.rabbits[0].food,31)
        self.failUnlessEqual(self.rabbits[0].speed,2)
        self.failUnlessEqual(self.rabbits[0].last_breed,7)

    def testFoxMigrate(self):
        numpy.random.seed(1)
        fox= agents.fox(age=2,food=10,pos=[5.5,5.5],speed=2,last_breed=7)
        fox.migrate(self.env)
        self.failUnlessAlmostEqual(fox.pos[0],3.765721,places=4,msg='Migrating fox has given different results from MATLAB')
        self.failUnlessAlmostEqual(fox.pos[1],6.496130,places=4,msg='Migrating fox has given different results from MATLAB')

class MATLABtest2(unittest.TestCase):
    #Compares results with a full MARTLAB run - ecolab(20,60,5,200) and rng(1)

    def testResults(self):
        numpy.random.seed(1)
        matlab_results = loadmat('fox_rabbit_20_60_5.mat')
        matlab_data = matlab_results['the_data']

        (agents,env,history) = ecolab.ecolab_matlab(size=20,nr=60,nf=5,steps=201)

        self.failUnless(all(history[0]==matlab_data[0]) and all(history[1]==matlab_data[1]),'Does not agree with MATLAB test data')
        

class FoxTests(unittest.TestCase):

    def setUP(self):
        pass

    def testDieOld(self):
        #Create an old fox
        fox= agents.fox(age=1000,food=10,pos=[5.5,5.5],speed=2,last_breed=7)
        
        fox.die()
        self.failUnless(fox.dead)
        
    def testDieStarve(self):
        #Create a starving fox
        fox= agents.fox(age=2,food=-1,pos=[5.5,5.5],speed=2,last_breed=7)
        #Ensure that it knows that its time to die
        fox.die()
        self.failUnless(fox.dead)

    def testEat(self):
        env= environment.environment(5)
        #Create a very fast fox
        fox= agents.fox(age=2,food=10,pos=[1.5,1.5],speed=10,last_breed=7)
        #create a rabbit very close to it
        rabbit_list = [agents.rabbit(age=2,food=10,pos=[1.52,1.52],speed=10,last_breed=7)]
        #Its almost certain that this fox ate this rabbit
        fox.eat(rabbit_list)
        #Doex rabbit know that its been eaten?
        self.failUnless(rabbit_list[0].has_been_eaten)
        #TODO - Make sure a slow fox doesn't eat a rabbit very far away

    def testBreed1(self):
        #Esnure that a fox that can breed, does breed

        #Create a fox that's ready to breed
        fox= agents.fox(age=30,food=100,pos=[5.5,5.5],speed=2,last_breed=21)
        new_fox = fox.breed()
        self.failUnless(isinstance(new_fox,agents.fox))

    def testBreed2(self):
        #Esnure that a breeding fox correctly distributes food

        #Create a fox that's ready to breed
        fox= agents.fox(age=30,food=100,pos=[5.5,5.5],speed=2,last_breed=21)
        new_fox = fox.breed()
        self.failUnless(fox.food == 50 and new_fox.food == 50)

    def testBreed3(self):
        #Esnure that a breeding fox correctly zeros last_breed

        #Create a fox that's ready to breed
        fox= agents.fox(age=30,food=100,pos=[5.5,5.5],speed=2,last_breed=21)
        new_fox = fox.breed()
        self.failUnless(new_fox.last_breed == 0 and new_fox.last_breed == 0)

    def testBreed4(self):
        #Esnure that a fox that is not ready to breed, doesn't

        #Create a fox that's not ready to breed doesn't
        fox= agents.fox(age=30,food=100,pos=[5.5,5.5],speed=2,last_breed=10)
        new_fox = fox.breed()
        self.failUnless(new_fox is None)


class RabbitTests(unittest.TestCase):

    def setUp(self):
        pass
        
    def testDefault(self):
        self.rabbit = agents.rabbit()
        self.assertEqual(self.rabbit.age,[])
        self.assertEqual(self.rabbit.food,[])
        self.assertEqual(self.rabbit.pos,[])
        self.assertEqual(self.rabbit.speed,[])
        self.assertEqual(self.rabbit.last_breed,[])

    def testDieOld(self):
        # Create an old rabbit
        rabbit= agents.rabbit(age=1000,food=10,pos=[5.5,5.5],speed=2,last_breed=7)
        # Ensure that it knows that its time to die
        rabbit.die()
        self.failUnless(rabbit.dead,'Ancient rabbit did not die')

    def testDieStarve(self):
        # Create a starving fox
        rabbit= agents.rabbit(age=2,food=-1,pos=[5.5,5.5],speed=2,last_breed=7)
        # Ensure that it knows that its time to die
        rabbit.die()
        self.failUnless(rabbit.dead,'Starved rabbit did not die')

    def testCpos(self):
        # Ensures cpos is calculated correctly
        self.rabbit1 = agents.rabbit(age=2,food=10,pos=[5.5,5.5],speed=2,last_breed=7) #In a food desert
        self.failUnless(all(self.rabbit1.cpos==5))

    def testEatInDesert(self):
        self.env = environment.environment(10)
        self.rabbit = agents.rabbit(age=2,food=10,pos=[5.5,5.5],speed=2,last_breed=7) #In a food desert
        #The rabbit is in a food desert. Does it eat correctly?
        starting_food = self.env.food[self.rabbit.cpos[0],self.rabbit.cpos[1]]
        self.failUnlessEqual(starting_food,0,'This rabbit was supposed to be in a desert')
        eaten = self.rabbit.eat(self.env)

        self.failUnlessEqual(self.env.food[self.rabbit.cpos[0],self.rabbit.cpos[1]],0,'Starting food was 0. Rabbit incorrectly changed that!')
        self.failIfEqual(eaten,1,'Rabbit reports that it has eaten when it can''t have')

    def testEatWhenHasFood(self):
         #The rabbit has some food.  Does it eat correctly?
        self.env = environment.environment(10)
        self.rabbit = agents.rabbit(age=2,food=10,pos=[1.2,1.2],speed=2,last_breed=7) #Food initially=50
        
        starting_food = self.env.food[(self.rabbit.cpos[0],self.rabbit.cpos[1])]
        self.failIfEqual(starting_food,0,'This rabbit was supposed to have access to food')
        
        eaten = self.rabbit.eat(self.env)

        self.failUnlessEqual(self.env.food[self.rabbit.cpos[0],self.rabbit.cpos[1]],starting_food-1,'Rabbit has incorrectly changed food quanity after eating.')

        self.failIfEqual(eaten,0,'Rabbit reports that it hasn''t eaten when it has')

    def testExtractLocalFoodTopLeftCorner(self):
        self.env = environment.environment(10)
        rabbit = agents.rabbit(age=2,food=10,pos=[1.1,1.1],speed=2,last_breed=7) #Rabbit in corner of simulation

        (local_food,xmin,ymin)  = rabbit.extract_local_food(self.env)

        self.failUnlessEqual(numpy.shape(local_food),(3,3),'Incorrect local food size for rabbit in top left corner')

        self.failUnless(numpy.all(local_food==50),'Incorrect local food values for rabbit in top left')

    def testExtractLocalFoodBottomRightCorner(self):
        self.env = environment.environment(10)
        rabbit = agents.rabbit(age=2,food=10,pos=[9.5,9.5],speed=2,last_breed=7) #Rabbit in corner of simulation
        
        (local_food,xmin,ymin)  = rabbit.extract_local_food(self.env)

        self.failUnlessEqual(numpy.shape(local_food),(3,3),'Incorrect local food size for rabbit in bottom right corner')

        correct = numpy.array([[0,50,50],[50,50,50],[50,50,50]])
        self.failUnless(numpy.array_equal(local_food,correct),'Incorrect local food values for rabbit in bottom right corner')

    def testExtractLocalFoodCentral(self):
        correct = [[50,50,50,50,50], \
               [50,50,50,50,50], \
               [50,50,50,50,50], \
               [50,50,50,0,0], \
               [50,50,50,0,0]]

        self.env = environment.environment(10)
        rabbit = agents.rabbit(age=2,food=10,pos=[5,5],speed=2,last_breed=7) 
        (local_food,xmin,ymin) = rabbit.extract_local_food(self.env)

        self.failUnless(numpy.array_equal(local_food,correct),'Incorrect local food values for rabbit in center')

    def testMigrateWhenFoodAvailable(self):
        #Does a rabbit at (5.5,5.5) migrate to the same position as the MATLAB version given that food is available
        self.env= environment.environment(10)
        numpy.random.seed(1) #MMigrate uses random numbers so need to seed to get reproducable results
        
        rabbit= agents.rabbit(age=2,food=10,pos=[5.5,5.5],speed=2,last_breed=7)
        rabbit.migrate(self.env)
        self.failUnlessAlmostEqual(rabbit.pos[0],4.917022,places=4,msg='Migrating rabbit has given different results from MATLAB')
        self.failUnlessAlmostEqual(rabbit.pos[1],5.22032449,places=4,msg='Migrating rabbit has given different results from MATLAB')

    def testMigrateWhenFoodNotAvailable(self):
        #Does a rabbit at (9.8,9.8) migrate to the same posiiton as the MATLAV version given that no food is available
        numpy.random.seed(1) #MMigrate uses random numbers so need to seed to get reproducable results
        
        self.env= environment.environment(10)
        self.env.food= numpy.zeros((10,10)) #Eat all the food
        rabbit= agents.rabbit(age=2,food=10,pos=[9.8,9.8],speed=2,last_breed=7)
        rabbit.migrate(self.env)
        
        self.failUnlessAlmostEqual(rabbit.pos[0],7.86930887,places=4,msg='Migrating rabbit has given different results from MATLAB')
        self.failUnlessAlmostEqual(rabbit.pos[1],9.27805005,places=4,msg='Migrating rabbit has given different results from MATLAB')

    def testBreed1(self):
        #Esnure that a rabbit that can breed, does breed

        #Create a rabbit that's ready to breed
        rabbit = agents.rabbit(age=30,food=100,pos=[5.5,5.5],speed=2,last_breed=21)
        new_rabbit = rabbit.breed()
        self.failUnless(isinstance(new_rabbit,agents.rabbit))


def main():
    unittest.main()

if __name__=='__main__':
    main()


