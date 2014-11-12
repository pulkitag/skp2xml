#include "xmlexporter.h"
#include <iostream>

int main(int argc, char* argv[]) {
  //Get Model Name
	if (argc < 2){
		std::cout << "argc is " << argc << "\n";
		std::cout<< "Usage: skp2xml input_file_name \n";
		return 1;
	}
	char* model_name = argv[1];

	std::string in_file(model_name);
	std::string out_file("tmp/out.xml");

	CXmlExporter model = CXmlExporter();
	model.Convert(in_file, out_file);

	return 0;
}
