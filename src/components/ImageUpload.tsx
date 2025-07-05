
import React, { useState, useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, X, Image as ImageIcon, Zap } from 'lucide-react';
import { apiEndpoints } from '@/config/api';
import { toast } from 'sonner';

interface ImageUploadProps {
  userId: string;
  onImageUpload: (filename: string) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ userId, onImageUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    setUploading(true);
    const fileArray = Array.from(files);
    
    for (const file of fileArray) {
      if (!file.type.startsWith('image/')) {
        toast.error(`${file.name} is not an image file`);
        continue;
      }

      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error(`${file.name} is too large (max 10MB)`);
        continue;
      }

      try {
        const formData = new FormData();
        formData.append('image', file);

        const response = await fetch(apiEndpoints.uploadImage, {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();

        if (response.ok) {
          setUploadedImages(prev => [...prev, data.filename]);
          onImageUpload(data.filename);
        } else {
          throw new Error(data.error || 'Upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    
    setUploading(false);
  }, [onImageUpload]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(e.target.files);
    }
  };

  const removeImage = (filename: string) => {
    setUploadedImages(prev => prev.filter(img => img !== filename));
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Upload className="w-5 h-5 mr-2" />
            Upload Item Images
          </CardTitle>
          <CardDescription>
            Drag and drop images or click to browse. AI will analyze your images to create compelling listings.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              dragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              disabled={uploading}
            />
            
            <div className="space-y-4">
              <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                <ImageIcon className="w-8 h-8 text-gray-400" />
              </div>
              
              <div>
                <p className="text-lg font-medium text-gray-900">
                  {dragActive ? 'Drop images here' : 'Drop images here or click to browse'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  PNG, JPG, GIF up to 10MB each
                </p>
              </div>
              
              {uploading && (
                <div className="flex items-center justify-center">
                  <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-2" />
                  <span className="text-blue-600">Uploading...</span>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Uploaded Images */}
      {uploadedImages.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Uploaded Images ({uploadedImages.length})</span>
              <Button className="bg-green-600 hover:bg-green-700">
                <Zap className="w-4 h-4 mr-2" />
                Generate AI Listings
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {uploadedImages.map((filename, index) => (
                <div key={filename} className="relative group">
                  <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <img
                      src={`http://localhost:8000/api/images/${filename}`}
                      alt={`Upload ${index + 1}`}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = '/placeholder.svg';
                      }}
                    />
                  </div>
                  
                  <button
                    onClick={() => removeImage(filename)}
                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X className="w-3 h-3" />
                  </button>
                  
                  <div className="mt-2">
                    <p className="text-xs text-gray-500 truncate">{filename}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ImageUpload;
