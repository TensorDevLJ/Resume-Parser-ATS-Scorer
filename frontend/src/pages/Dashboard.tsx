import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const data = [
  { name: 'Skill Match', value: 85 },
  { name: 'Experience', value: 75 },
  { name: 'Projects', value: 80 },
  { name: 'Education', value: 90 },
]

const skillData = [
  { name: 'Matched', value: 35, fill: '#10B981' },
  { name: 'Missing', value: 12, fill: '#EF4444' },
  { name: 'Extra', value: 8, fill: '#F59E0B' },
]

export default function Dashboard() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">ATS Score Breakdown</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Skills Analysis</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={skillData} dataKey="value" cx="50%" cy="50%" outerRadius={80} label>
                {skillData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <div className="text-3xl font-bold text-blue-600">85</div>
          <div className="text-gray-600">Overall ATS Score</div>
        </div>
        <div className="bg-green-50 p-6 rounded-lg border border-green-200">
          <div className="text-3xl font-bold text-green-600">35</div>
          <div className="text-gray-600">Matched Skills</div>
        </div>
        <div className="bg-red-50 p-6 rounded-lg border border-red-200">
          <div className="text-3xl font-bold text-red-600">12</div>
          <div className="text-gray-600">Missing Skills</div>
        </div>
        <div className="bg-amber-50 p-6 rounded-lg border border-amber-200">
          <div className="text-3xl font-bold text-amber-600">3</div>
          <div className="text-gray-600">Resumes Uploaded</div>
        </div>
      </div>
    </div>
  )
}
