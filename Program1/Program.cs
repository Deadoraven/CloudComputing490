using System;
using System.Net;
using System.Net.Http;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace SimpleCrawl
{
    class Program
    {
        static Dictionary<string, bool> visitedLinks = new Dictionary<string, bool>();
        static int hopNumber = 0;
        static int counter = 0;
        static string tagPattern = @"<a href=""((http:\/\/w*\.?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z\/]{2,6}\b)([-a-zA-Z0-9@:%_\+.~#?&=\/]*))";
        static string linkPattern = @"(https?:\/\/w*\.?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z\/]{2,6}\b)([-a-zA-Z0-9@:%_\+.~#?&=\/]*)";
        static void Main(string[] args)
        {
            //string addr = "http://courses.washington.edu/css342/dimpsey";
            string addr = args[0];
            Match webAddress = Regex.Match(addr, linkPattern);

            string uri = webAddress.Groups[1].Value;
            string url = webAddress.Groups[2].Value;

            Console.WriteLine("Making API call...");
            Console.WriteLine(counter++ + ":Started at address: " + webAddress);
            visitedLinks.Add(webAddress.Value, true);

            hopNumber = int.Parse(args[1]);
            //hopNumber = 600;
            Get(uri, url);

        }

        public static void Get(string uri, string url)
        {

            string result = "";
            using (var client = new HttpClient(new HttpClientHandler { AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate }))
            {
                client.BaseAddress = new Uri(uri);
                HttpResponseMessage response = client.GetAsync(url).Result;
                response.EnsureSuccessStatusCode();
                result = response.Content.ReadAsStringAsync().Result;
            }

            if (hopNumber == 0)
            {
                Console.WriteLine("--------------------------------------------------------------");
                Console.WriteLine(result);
                Console.WriteLine("--------------------------------------------------------------");
                return;
            }
            else
            {
                Match match = Regex.Match(result, tagPattern);

                while (match.Success)
                {
                    string newAddr = match.Groups[1].Value;
                    if (!visitedLinks.ContainsKey(match.Value))
                    {
                        visitedLinks.Add(match.Value, true);

                        string newUri = match.Groups[2].Value;
                        string newUrl = match.Groups[3].Value;

                        Console.WriteLine(counter++ + ":hopped at: " + match.Groups[1].Value);
                        hopNumber--;
                        Get(newUri, newUrl);
                        if (hopNumber == 0)
                        {
                            break;
                        }
                    }
                    else match.NextMatch();
                    match = match.NextMatch();
                }
                return;
            }
        }
    }
}