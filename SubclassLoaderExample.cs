using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace SubclassLoader
{
    #region ExampleClasses
    class Parent 
    {
        public virtual string Run() => "Default run";
        
    }
    class ChildA : Parent 
    {
        public override string Run() => "Muha i'm the first child";
    }
    class ChildB : Parent 
    {
        public override string Run() => "Mahw i was second";
    }
    class ChildC : Parent 
    {
        public override string Run() => "Well last but not least";
    }
    #endregion

    #region Main
    class Program
    {
        // Fetch sub instances as enumerator
        static IEnumerable<T> GetSubclassInstances<T>()
        {
            foreach (System.Type subType in Assembly.GetExecutingAssembly()
                                                    .GetTypes()
                                                    .Where(type => type.IsSubclassOf(typeof(Parent))))
                yield return (T)Activator.CreateInstance(subType);
        }
        
        static void Main(string[] args)
        {
            /**
             * Output:
             * - ChildA
             * - ChildB
             * - ChildC
             * 
             * && foreach -> Run override output
             */
             // Load class types using assembly
            List<System.Type> childTypes = Assembly.GetExecutingAssembly()
                .GetTypes()
                .Where(type => type.IsSubclassOf(typeof(Parent)))
                .ToList();

            childTypes.ForEach(type =>
            {
                Console.WriteLine($"Type: {type.FullName}");

                // Create an instance based upon child type using Activator
                object instance = Activator.CreateInstance(type);
                if (instance != null) Console.WriteLine($"Run output: {((Parent)instance).Run()}"); // Cast object to parent class -> run overiden method.
      
                // Line Break.
                Console.WriteLine(string.Join("", Enumerable.Repeat('-', Console.WindowWidth-1)));
            });

            
        }
    }
    #endregion
}
