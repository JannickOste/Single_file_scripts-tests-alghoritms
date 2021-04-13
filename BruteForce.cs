    class Program
    {
        private static string _password = "myp";
        private static bool _is_found = false;
        private static char[] _character_table = {
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
            '6', '7', '8', '9', '0', '!', '$', '#', '@', '-'
        };

        public static string output { get; private set; }
        public static int attempts { get; private set; }

        public static void Main(string[] args)
        {
            DateTime start_time = DateTime.Now;
            attempts = 0;
            Console.WriteLine($"Starting bruteforce attempt at: {start_time}");


            int current_password_length = 0;
            while (!_is_found)
            {
                current_password_length += 1;
                GenerateKey(0,
                    Enumerable.Range(0, current_password_length).Select(_ => _character_table[0]).ToArray(),
                    current_password_length, current_password_length - 1);
            }

            Console.WriteLine($"Password: {output}");
            Console.WriteLine($"Password found in: {DateTime.Now.Subtract(start_time)}");
        }

        public static void GenerateKey(int position, char[] key_characters, int password_length, int last_index)
        {
            int next_position = position;

            foreach(char chr in _character_table)
            {
                key_characters[position] = chr;

                if (position < last_index)
                    GenerateKey(position + 1, key_characters, password_length, last_index);
                else
                {
                    attempts++;

                    if (new String(key_characters) == _password)
                    {
                        _is_found = true;
                        output = new String(key_characters);
                    }
                }
            }
        }
     
    }
