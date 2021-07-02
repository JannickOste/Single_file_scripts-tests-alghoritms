using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace SubclassLoader
{
    #region ExampleClasses
    class Parent           { public virtual string Run()  => "Default run"; }
    class ChildA : Parent  { public override string Run() => "Muha i'm the first child"; }
    class ChildB : Parent  { public override string Run() => "Mahw i was second"; }
    class ChildC : Parent  { public override string Run() => "Well last but not least"; }
    #endregion

    #region Main
    class Program
    {
        static IEnumerable<System.Type> GetSubclassTypes<T>() => Assembly.GetExecutingAssembly()
                                                                            .GetTypes()
                                                                            .Where(type => type.IsSubclassOf(typeof(T)))
                                                                            .AsEnumerable<System.Type>();

        static IEnumerable<T> GetSubclassInstances<T>() => GetSubclassTypes<T>()
                                                            .Select(t => (T)Activator.CreateInstance(t))
                                                            .AsEnumerable<T>();

        static void Main(string[] args)
        {
            foreach(Parent child in GetSubclassInstances<Parent>())
                Console.WriteLine($"Subclass type: {child.GetType().Name}\n" +
                                  $"Subclass run output: {child.Run()}\n" +
                                  $"{string.Join("", Enumerable.Repeat('-', Console.WindowWidth - 1))}");

            
        }
    }
    #endregion
}
