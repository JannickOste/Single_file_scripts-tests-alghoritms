    internal abstract class LogicGate
    {
        // Create attribute for auto load.
        private class GateAttribute : Attribute {};

        #region Logic gate functions
        [Gate] public static bool NOT(bool a)         => !a;
        [Gate] public static bool AND(bool a, bool b) => a && b;
        [Gate] public static bool OR (bool a, bool b) => a || b;
        [Gate] public static bool XOR(bool a, bool b) => (a && !b) || (!a && b);
        [Gate] public static bool NAND(bool a, bool b) => NOT(AND(a, b));
        [Gate] public static bool NOR(bool a, bool b) => NOT(OR(a, b));
        [Gate] public static bool XNOR(bool a, bool b) => NOT(XOR(a, b));
        #endregion

        #region Testing methods and variables
        private static (bool a, bool b)[] grid = new (bool a, bool b)[]{
            (false, false),
            (false, true),
            (true, false),
            (true, true)
        };
        
        public static void TestGates()
        {
            foreach(MethodInfo callback in typeof(LogicGate).GetMethods(BindingFlags.Static | BindingFlags.Public)
                                                            .Where(i => i.GetCustomAttribute(typeof(GateAttribute), false) != null))
            {
                int bool_parameter_count = callback.GetParameters().Count(i => i.ParameterType == typeof(bool));
                if(bool_parameter_count == 0 | bool_parameter_count > 2) continue;

                Console.WriteLine($"[Output]: {callback.Name}");
                Console.WriteLine(bool_parameter_count == 1 ? "A | Y" : "A | B | Y");
                if(bool_parameter_count == 1)
                {
                    for(int i = 0; i < 2; i++)
                    {
                        bool y = (bool)callback.Invoke(obj: null, parameters: new object[]{i != 0});
                        Console.WriteLine($"{(i != 0 ? '1' : '0')} | {(y ? '1' : '0')}");
                    }
                }
                else
                {
                    foreach((bool a, bool b) set in grid)
                    {
                        bool y = (bool)callback.Invoke(obj: null, parameters: new object[]{set.a, set.b});
                        Console.WriteLine($"{(set.a ? '1' : '0')} | {(set.b ? '1' : '0')} | {(y ? '1' : '0')}");
                    }
                }
            }
        }
        #endregion
    }
