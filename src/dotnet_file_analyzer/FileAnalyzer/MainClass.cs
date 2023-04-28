using System;
using System.Linq;

namespace FileAnalyzer
{
    public class AnalyzedFile
    {
        public byte[] raw_file_bytes;
        public long[,] digraph_image = new long[256, 256];

        public AnalyzedFile(string path)
        {
            raw_file_bytes = System.IO.File.ReadAllBytes(path);
        }

        public void generate_2D_digraph_image()
        {
            foreach (Tuple<byte, byte> byte_tuple in raw_file_bytes.Zip(raw_file_bytes.Skip(1), Tuple.Create))
            {
                int index1 = byte_tuple.Item1;
                int index2 = byte_tuple.Item2;
                digraph_image[index1, index2] += 1;
            }
        }
    }
}