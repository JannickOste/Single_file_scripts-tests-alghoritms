
    class Program
    {
        /**
         * Check two strings of equal length and check the distance based on the character diffrentiating. 
         */
        public static int hammingDistance(string target, string input)
        {
            if (target.Length != input.Length) throw new ArgumentException("Strings must be of equal length.");
            return Enumerable.Range(0, target.Length).Select(i => target[i] == input[i]).Count(i => i == false);
        }

        /**
         * Levenstein alghortim checks the number of edits required to change the input to the target - 
         *  using insertion, deletion & subtition and calculates the distance of string two to string one based on this.
         */
        public static int levensteinCompare(string target, string input)
        {
            int distance = 0;
            for (int i = 0; i < target.Length; i++)
            {
                if (input[i] != target[i]) distance++;
                if (i == input.Length || i == target.Length-1 & i < input.Length-1)
                {
                    if (i != Math.Max(input.Length, target.Length))
                        distance += Math.Max(input.Length, target.Length) - Math.Min(input.Length, target.Length);
                    break;
                }
            }
            return distance;
        }


        /**
         * damaruaLevensthein alghoritms checks the number of edits required to change the input to the target - 
         *   using insertion, deletion & transportation instead of subjegating each character to another like the levensthein alghoritm does.
         */
        public int damaruaLevenstheinDistance(string target, string input)
        {
            var arrayDimension = new int[target.Length, input.Length];

            for (var i = 0; i < target.Length; i++) arrayDimension[i, 0] = i;
            for (var j = 0; j < input.Length; j++) arrayDimension[0, j] = j;

            // Starting at 1 to avoid ArgumentOutOfRangeException when checking previous character.
            for(var i = 1; i < target.Length; i++)
                for(var j = 1; j < input.Length; j++)
                {
                    // Check character equality.
                    var equalityCost = target[i] == input[i] ? 0 : 1;

                    // Calculate the costs.
                    var deleteCost = arrayDimension[i - 1, j] + 1;
                    var insertionCost = arrayDimension[i, j - 1] + 1;
                    var replacementCost = arrayDimension[i - 1, j - 1] + equalityCost;
                    
                    arrayDimension[i, j] = (deleteCost = deleteCost < insertionCost ? deleteCost : insertionCost) < replacementCost ? deleteCost : replacementCost;

                    // Transformation / Permutation
                    if (i > 1 && j > 1 && target[i-1] == input[i-2] && target[i-2] == input[i-1])
                    {
                        arrayDimension[i, j] = Math.Min(arrayDimension[i, j], arrayDimension[i - 2, j - 2] + equalityCost);
                    }
                }
            return arrayDimension[target.Length - 1, input.Length - 1];
        }

        static void Main(string[] args)
        {
            /*
            List<string> splitter = new List<string>() { "test", "one", "two"};
            Console.WriteLine(splitter.Count > 2 ? String.Join(".", splitter.GetRange(0, splitter.Count - 1)) : splitter[0]);
            */
            // Console.WriteLine(levensteinCompare("tost", "testee"));
            // Console.WriteLine(hammingDistance("test", "tost"));
            string target = "test my";
            string input = "moy test";

            Console.WriteLine("Target: {0}\n" +
                              "Input: {1}\n" +
                              "Levensthein distance: {2}\n" +
                              "Damerau-Levensthein distance: {3}", 
            target, input, levensteinCompare(target, input), damaruaLevenstheinCompare(input, target));

        }
    }
