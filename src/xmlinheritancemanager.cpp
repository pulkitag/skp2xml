// Copyright 2013 Trimble Navigation Limited. All Rights Reserved.

#include <assert.h>

#include "xmlinheritancemanager.h"
#include <slapi/model/component_definition.h>
#include <slapi/model/component_instance.h>
#include <slapi/model/drawing_element.h>
#include <slapi/model/edge.h>
#include <slapi/model/entity.h>
#include <slapi/model/face.h>
#include <slapi/model/group.h>
#include <slapi/model/layer.h>
#include <slapi/model/material.h>

using namespace XmlGeomUtils;

CInheritanceManager::CInheritanceManager() {
  materials_by_layer_ = false;
}

CInheritanceManager::CInheritanceManager(bool by_layer) {
  materials_by_layer_ = by_layer;
}

CInheritanceManager::~CInheritanceManager() {
}

void CInheritanceManager::PushMaterial(SUDrawingElementRef drawing_element) {
  SUMaterialRef material;
  SUSetInvalid(material);
  SUDrawingElementGetMaterial(drawing_element, &material);
  front_materials_.push_back(material);       
  back_materials_.push_back(material);

  SUColor color = { 0 };
  SUMaterialGetColor(material, &color);
  edge_colors_.push_back(color);
}

void CInheritanceManager::PushLayer(SUDrawingElementRef drawingElementRef) {
  SULayerRef layer;
  SUSetInvalid(layer);
  SUDrawingElementGetLayer(drawingElementRef, &layer);
  layers_.push_back(layer);
}

void CInheritanceManager::PushElement(SUGroupRef group) {
  // Material & Layer
  SUDrawingElementRef drawing_element = SUGroupToDrawingElement(group);
  PushMaterial(drawing_element);
  PushLayer(drawing_element);
}

void CInheritanceManager::PushElement(SUFaceRef face) {
  // Front Material
  SUMaterialRef front_material = SU_INVALID;
  SUFaceGetFrontMaterial(face, &front_material);
  front_materials_.push_back(front_material);

  // Back Material
  SUMaterialRef back_material = SU_INVALID;
  SUFaceGetBackMaterial(face, &back_material);
  back_materials_.push_back(back_material);

  // Edge color, none
  SUColor color = { 0 };
  edge_colors_.push_back(color);

  // Layer
  SULayerRef layer = SU_INVALID;
  SUDrawingElementGetLayer(SUFaceToDrawingElement(face), &layer);
  layers_.push_back(layer);
}

void CInheritanceManager::PushElement(SUEdgeRef edge) {
  // Materials
  SUMaterialRef material = SU_INVALID;
  front_materials_.push_back(material);
  back_materials_.push_back(material);

  // Edge color
  SUColor color = { 0 };
  SUEdgeGetColor(edge, &color);
  edge_colors_.push_back(color);

  // Layer
  SULayerRef layer = SU_INVALID;
  SUDrawingElementGetLayer(SUEdgeToDrawingElement(edge), &layer);
  layers_.push_back(layer);
}

void CInheritanceManager::PopElement() {
  // Materials
  assert(front_materials_.size() > 0);
  front_materials_.pop_back();

  assert(back_materials_.size() > 0);
  back_materials_.pop_back();

  // Edge color
  assert(edge_colors_.size() > 0);
  edge_colors_.pop_back();

  // Layers
  assert(layers_.size() > 0);
  layers_.pop_back();
}

SULayerRef CInheritanceManager::GetCurrentLayer() const {
  // Search layer stack for first non-null layer
  int n = static_cast<int>(layers_.size());
  for (int i = n; --i >= 0;) {
    if (!SUIsInvalid(layers_[i])) {
      return layers_[i];
    }
  }
  SULayerRef layer = SU_INVALID;
  return layer;
}

SUMaterialRef CInheritanceManager::GetCurrentFrontMaterial() const {
  SUMaterialRef material = SU_INVALID;
  if (materials_by_layer_) {
    SULayerRef layer = GetCurrentLayer();
    if (SU_ERROR_NONE == SULayerGetMaterial(layer, &material)) {
      return material;
    }
  } else {
    // Search material stack for first valid material
    int n = static_cast<int>(front_materials_.size());
    for (int i = n; --i >= 0;) {
      if (!SUIsInvalid(front_materials_[i])) {
        return front_materials_[i];
      }
    }
  }
  return material;
}

SUMaterialRef CInheritanceManager::GetCurrentBackMaterial() const {
  SUMaterialRef material = SU_INVALID;
  if (materials_by_layer_) {
    SULayerRef layer = GetCurrentLayer();
    if (SU_ERROR_NONE == SULayerGetMaterial(layer, &material)) {
      return material;
    }
  } else {
    // Search material stack for first non-null layer
    int n = static_cast<int>(back_materials_.size());
    for (int i = n; --i >= 0;) {
      if (!SUIsInvalid(back_materials_[i])) {
        return back_materials_[i];
      }
    }
  }
  return material;
}

SUColor CInheritanceManager::GetCurrentEdgeColor() const {
  SUColor color = { 0 };
  SUMaterialRef material = SU_INVALID;
  if (materials_by_layer_) {
    SULayerRef layer = GetCurrentLayer();
    if (SU_ERROR_NONE == SULayerGetMaterial(layer, &material)) {
      SUMaterialGetColor(material, &color);
    }
  } else {
    // Search material stack for first non-null layer
    int n = static_cast<int>(edge_colors_.size());
    if (n > 0) {
      color = edge_colors_.back();
    }
  }
  return color;
}
