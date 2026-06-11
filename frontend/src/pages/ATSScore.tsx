export default function ATSScore() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold mb-4">ATS Score Calculator</h1>
        <p className="text-gray-600 mb-8">Compare your resume against a job description</p>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Your Resume</label>
            <select className="w-full border rounded-lg p-2">
              <option>Select a resume...</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Job Description</label>
            <textarea className="w-full border rounded-lg p-2 h-32" placeholder="Paste job description..." />
          </div>
        </div>

        <button className="bg-blue-600 text-white px-8 py-2 rounded-lg hover:bg-blue-700 w-full font-semibold">
          Calculate Score
        </button>
      </div>
    </div>
  )
}
