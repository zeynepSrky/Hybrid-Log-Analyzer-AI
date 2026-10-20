using System;
using System.IO;
using System.Text;
using System.Net.Http;
using System.Threading.Tasks; //main metodun async olacaksa
using System.Text.Json;
using System.Reflection.Metadata.Ecma335;
class Program
{
    public static async Task Main()
    {
        using HttpClient client = new HttpClient();
        string url_local = "http://127.0.0.1:5000/predict";
        string path = @"ornek.txt";

        if (!File.Exists(path))
        {
            string[] createText = {"ornek.txt"};
            File.WriteAllLines(path, createText);
        }

        string[] readText = File.ReadAllLines(path);
        foreach (string s in readText)
        {
            var payload = new {log = s};
            string jsonBody = JsonSerializer.Serialize(payload);
            HttpContent content = new StringContent(jsonBody, Encoding.UTF8, "application/json");

            HttpResponseMessage response = await client.PostAsync(url_local, content);
            string result = await response.Content.ReadAsStringAsync();
            //Console.WriteLine("Pythondan gelen cevap: " + result);

            if(result.Contains("Tehdit"))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"[!] Tehdit Algılandı: {s} -> {result}");
            }
            else if(result.Contains("Normal"))
            {
                Console.ForegroundColor= ConsoleColor.Green;
                Console.WriteLine($"[+] Güvenli Trafik: {s} -> {result}");
            }
            Console.ResetColor();
        }

    }
}

