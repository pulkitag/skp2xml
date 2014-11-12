// Copyright 2013 Trimble Navigation Limited. All Rights Reserved.

#ifndef SKPTOXML_COMMON_XMLEXPORTER_H
#define SKPTOXML_COMMON_XMLEXPORTER_H

#include "xmlinheritancemanager.h"
#include "xmloptions.h"
#include "xmlstats.h"
#include "xmlfile.h"

#include <slapi/model/defs.h>

class CXmlExporter {
 public:
  CXmlExporter();
  virtual ~CXmlExporter();

  // Convert
  bool Convert(const std::string& from_file,
               const std::string& to_file);

  // Set user options
  void SetOptions(const CXmlOptions& options) { options_ = options; }

  // Get stats
  const CXmlExportStats& stats() const { return stats_; }

private:
  // Clean up slapi objects
  void ReleaseModelObjects();

  // Write texture files to the destination directory
  void WriteTextureFiles();

  void WriteLayers();
  void WriteLayer(SULayerRef layer);

  void WriteMaterials();
  void WriteMaterial(SUMaterialRef material);

  void WriteComponentDefinitions();
  void WriteComponentDefinition(SUComponentDefinitionRef comp_def);

  void WriteGeometry();
  void WriteEntities(SUEntitiesRef entities);
  void WriteFace(SUFaceRef face);
  void WriteEdge(SUEdgeRef edge);
  void WriteCurve(SUCurveRef curve);

  XmlEdgeInfo GetEdgeInfo(SUEdgeRef edge) const;

private:
  CXmlOptions options_;

  // Export statistics. Filled in by this exporters class and used later by
  // the platform specific plugin classes to populate the results dialog.
  CXmlExportStats stats_;

  // SLAPI model and texture writer
  SUModelRef model_;
  SUTextureWriterRef texture_writer_;

  // Stack
  CInheritanceManager inheritance_manager_;

  // File & stats
  CXmlFile file_;
};

#endif // SKPTOXML_COMMON_XMLEXPORTER_H
