
import React, { useState, useCallback, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, X, Image as ImageIcon, Zap, AlertCircle } from 'lucide-react';
import { apiEndpoints } from '@/config/api';
import { toast } from 'sonner';
import { useQuery } from '@tanstack/react-query';

interface ImageUploadProps {
  userId: string;
  onImageUpload: (filename: string) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ userId, onImageUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);

  // Get user's draft images
  const { data: drafts = [], refetch: refetchDrafts } = useQuery({
    queryKey: ['userDrafts', userId],
    queryFn: async () => {
      const response = await fetch(apiEndpoints.getUserDrafts(userId));
      if (!response.ok) return [];
      const data = await response.json();
      return data.drafts || [];
    },
    enabled: !!userId
  });

  const remainingSlots = 10 - drafts.length;

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    
    // Check if adding these files would exceed the limit
    if (drafts.length + fileArray.length > 10) {
      toast.error(`You can only have 10 draft images total. You have ${drafts.length} drafts and are trying to add ${fileArray.length} more.`);
      return;
    }

    setUploading(true);
    
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
        formData.append('user_id', userId);

        const response = await fetch(apiEndpoints.uploadDraftImage, {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();

        if (response.ok) {
          onImageUpload(data.filename);
          toast.success(`${file.name} saved as draft`);
        } else {
          throw new Error(data.error || 'Upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    
    setUploading(false);
    refetchDrafts();
  }, [userId, drafts.length, onImageUpload, refetchDrafts]);

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

  const removeDraft = async (filename: string) => {
    try {
      const response = await fetch(apiEndpoints.deleteDraftImage(userId, filename), {
        method: 'DELETE'
      });

      if (response.ok) {
        toast.success('Draft deleted');
        refetchDrafts();
      } else {
        throw new Error('Failed to delete draft');
      }
    } catch (error) {
      console.error('Error deleting draft:', error);
      toast.error('Failed to delete draft');
    }
  };

  const generateListings = async () => {
    if (drafts.length === 0) {
      toast.error('No draft images to process');
      return;
    }

    try {
      const response = await fetch(apiEndpoints.generateListings, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          image_filenames: drafts.map(draft => draft.filename)
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(`Generated ${data.listings_created} AI listings from your drafts!`);
        refetchDrafts(); // Refresh to show updated state
      } else {
        throw new Error(data.error || 'Failed to generate listings');
      }
    } catch (error) {
      console.error('Error generating listings:', error);
      toast.error('Failed to generate AI listings');
    }
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Upload className="w-5 h-5 mr-2" />
              Upload Item Images
            </div>
            <div className="text-sm font-normal text-gray-500">
              {drafts.length}/10 draft slots used
            </div>
          </CardTitle>
          <CardDescription>
            Drag and drop images or click to browse. Images are saved as drafts until you create eBay listings.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {remainingSlots === 0 ? (
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center bg-gray-50">
              <AlertCircle className="w-8 h-8 text-gray-400 mx-auto mb-4" />
              <p className="text-lg font-medium text-gray-600 mb-2">
                Draft Limit Reached
              </p>
              <p className="text-sm text-gray-500">
                You have 10 draft images. Delete some drafts or create listings to upload more.
              </p>
            </div>
          ) : (
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
                disabled={uploading || remainingSlots === 0}
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
                    PNG, JPG, GIF up to 10MB each • {remainingSlots} slots remaining
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
          )}
        </CardContent>
      </Card>

      {/* Draft Images */}
      {drafts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Draft Images ({drafts.length})</span>
              <Button 
                onClick={generateListings}
                className="bg-green-600 hover:bg-green-700"
              >
                <Zap className="w-4 h-4 mr-2" />
                Generate AI Listings
              </Button>
            </CardTitle>
            <CardDescription>
              These images are saved as drafts. Generate listings to post on eBay.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {drafts.map((draft, index) => (
                <div key={draft.filename} className="relative group">
                  <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <img
                      src={apiEndpoints.getImage(draft.filename)}
                      alt={`Draft ${index + 1}`}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = '/placeholder.svg';
                      }}
                    />
                  </div>
                  
                  <button
                    onClick={() => removeDraft(draft.filename)}
                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <X className="w-3 h-3" />
                  </button>
                  
                  <div className="mt-2">
                    <p className="text-xs text-gray-500 truncate">{draft.filename}</p>
                    <p className="text-xs text-blue-600">Draft</p>
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
