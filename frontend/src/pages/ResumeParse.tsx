import { Upload, FileText, CheckCircle } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'

export default function ResumeParse() {
  const [uploading, setUploading] = useState(false)
  const [parsed, setParsed] = useState(null)

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('/api/resume/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setParsed(data)
        toast.success('Resume parsed successfully!')
      } else {
        toast.error('Failed to parse resume')
      }
    } catch (error) {
      toast.error('Error uploading file')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold mb-2">Parse Resume</h1>
        <p className="text-gray-600 mb-6">Upload your resume to extract all information automatically</p>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition">
          <input
            type="file"
            accept=".pdf,.docx,.doc"
            onChange={handleUpload}
            disabled={uploading}
            className="hidden"
            id="file-input"
          />
          <label htmlFor="file-input" className="cursor-pointer">
            <Upload size={48} className="mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-semibold mb-2">
              {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
            </p>
            <p className="text-gray-500">PDF, DOCX or DOC (Max 10MB)</p>
          </label>
        </div>

        {parsed && (
          <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="text-green-600" size={24} />
              <h2 className="text-lg font-semibold">Parsing Complete</h2>
            </div>
            <div className="space-y-2 text-gray-700">
              <p><strong>Name:</strong> {parsed.name || 'Not found'}</p>
              <p><strong>Email:</strong> {parsed.email || 'Not found'}</p>
              <p><strong>Skills:</strong> {parsed.skills?.join(', ') || 'Not found'}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
