export default function SkillGap() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow p-8">
        <h1 className="text-3xl font-bold mb-4">Skill Gap Analysis</h1>
        <p className="text-gray-600 mb-8">Identify missing and recommended skills</p>

        <div className="space-y-6">
          <div>
            <h2 className="text-lg font-semibold mb-4 text-green-600">Matched Skills (35)</h2>
            <div className="flex flex-wrap gap-2">
              {['Python', 'React', 'FastAPI', 'PostgreSQL', 'Docker'].map(skill => (
                <span key={skill} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-4 text-red-600">Missing Skills (12)</h2>
            <div className="flex flex-wrap gap-2">
              {['Kubernetes', 'AWS', 'GraphQL', 'Redis'].map(skill => (
                <span key={skill} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold mb-4 text-blue-600">Recommended Skills</h2>
            <div className="flex flex-wrap gap-2">
              {['Terraform', 'CI/CD', 'Microservices', 'Machine Learning'].map(skill => (
                <span key={skill} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
