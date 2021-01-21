using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;

namespace WifiPassDumper
{
    class Program
    {
        static Process getDosProcess(string input = "")
        {
            var p = new Process();
            p.StartInfo.FileName = "C:\\windows\\system32\\cmd.exe";
            p.StartInfo.Arguments = $"/C {input}";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = true;
            p.StartInfo.CreateNoWindow = true;
            return p;
        }

        static Dictionary<string, string> getDosOutput(string input)
        {
            using(var p = getDosProcess(input))
            {
                //Start & excecute process
                p.Start();
                p.WaitForExit();
                System.Threading.Thread.Sleep(2000);
                //Output Parse
                var stdout = p.StandardOutput.ReadToEnd();
                var output = stdout.Length > 0 ? stdout : p.StandardError.ReadToEnd();

                //Result parse
                return new Dictionary<string, string>()
                {
                    { "output", output },
                    { "error_level", stdout.Length > 0 ? "0" : "1"}
                };
            }
        }

        static Dictionary<string, string> fetchWifiPassword()
        {
            Dictionary<string, string> passlib = new Dictionary<string, string>();

            string res = getDosOutput("netsh wlan show profile")["output"].Split("\n").Where(i => i.Contains("All User Profile")).FirstOrDefault();
            res.Substring(res.IndexOf(":") + 1).Split().Where(i => i.Length > 0).ToList().ForEach(profile =>
            {
                var pasres = getDosOutput($"netsh wlan show profile {profile} key=clear")["output"].Split("\n").Where(i => i.Contains("Key Content")).FirstOrDefault();
                passlib.Add(profile, pasres.Substring(pasres.IndexOf(":") + 2));
            });

            return passlib;
        }
        static void Main(string[] args)
        {
            var password = fetchWifiPassword();
            if (password.Count() == 0) Console.WriteLine("Failed to find profile presets, have you been connected to any networks before?");
            else
            {
                var lineout = password.Select(i => $"{i.Key}: {i.Value}").ToList();
                lineout.Insert(0, "[Wifi Password]:");
                lineout.Add("\nPress any key to close window.");
                Console.WriteLine(String.Join("\n", lineout));
                System.IO.File.Create("password.txt");
                Console.ReadKey();
            }
        }
    }
}
