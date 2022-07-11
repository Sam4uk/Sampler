#!/usr/bin/python
# script for genete samples
import sys, getopt, os

def main(argv):
    inputfile = ''
    outputfile = ''

    hint_string_use = 'run sampler with param "-h" for more info'
    hint_help = '\n\t sampler.py -i <inputfile> -o <outputfile>'
    hint_help += '\n\t <inputfile> \t any file name for sampling to c/c++ header file'
    hint_help += '\n\t <outputfile> \t filename of c/c++ header file. Please set extension manualy'
    hint_help += '\n\n================= EXAMPLE OF USE ================='
    hint_help += '\n$>./sampler.py -i samefile.ext -o sampe_of_file.h '
    hint_help += '\n                    or'
    hint_help += '\n$>python ./sampler.py -i samefile.ext             '
    hint_help += '\n\n\t when <outputfile> is empy output file name is a same'
    hint_help += '\n\t with double extension \'<filename_with_ext>.h\''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print (hint_string_use)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (hint_help)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if (inputfile==""):
        print (hint_string_use)
        sys.exit(1)
    if (outputfile==""):
        outputfile=inputfile+".h"
        print ('Output file name not set. Using default filename as', outputfile)
    try:
        def sampleID(id):
            return "SAMPLE_"+id

        def define (name, value, par=""):
            if (par==""):
                return "#define " + name + " " + value + "\n"
            else:
                return "#define " + name + "("+ par+") " + value + "\n"

        def data(filename,size):
            if (size==0):
                res = "{}"
            else:
                line = 12
                if (size < (line)):
                    res = "{"
                else:
                    res = "{\\\n    "
                with open(filename, "rb") as f:
                    for x in range(size-1):
                        byte = f.read(1)
                        if  ((x % line) == line - 1):
                            res += hex(ord(byte)) + ",\t\t\t\t\\\n    "
                        else:
                            res += hex(ord(byte)) + ", "
                    byte = f.read(1)
                    res += hex(ord(byte))
                    if (size < line):
                        res += "}\n"
                    else:
                        res += "\t\t\t\t\\\n}"
            return res


        def header (id, filename, name):
            res = ""
            res += "#ifndef "+ sampleID(id)+"_H\n"
            res += define( sampleID(id) + "_H", "(1)")
            res += define(sampleID(id) + "_SIZE", "(" + str(os.stat(filename).st_size) + ") /**<= size of sample*/")
            res += define(sampleID(id) + "_DATA", data(filename,os.stat(filename).st_size))
            res += define(sampleID(id) + "_TYPE", "const uint8_t  /**<= type of data*/")
            res += define(sampleID(id) + "_USE", sampleID(id) + "_TYPE " + "SAMPLE_NAME" + "[" + sampleID(id) + "_SIZE]" + sampleID(id) + "_DATA","SAMPLE_FILE_NAME" )
            res += "\n#endif\n"
            return res 

        header_file = open(outputfile,"w")
        header_file.write(header("FILE",inputfile, "nameis"));
        header_file.close()

    except IOError:
        print ('Error While Opening the file!')

if __name__ == "__main__":
   main(sys.argv[1:])