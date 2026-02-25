'use client';

import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, AlertTriangle, TrendingUp, Users, Clock } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const crowdData = [
  { time: '00:00', crowd: 2400, prediction: 2210 },
  { time: '04:00', crowd: 1398, prediction: 2290 },
  { time: '08:00', crowd: 9800, prediction: 2000 },
  { time: '12:00', crowd: 3908, prediction: 2108 },
  { time: '16:00', crowd: 4800, prediction: 2200 },
  { time: '20:00', crowd: 3800, prediction: 2100 },
  { time: '23:59', crowd: 4300, prediction: 2300 },
];

const templeMetrics = [
  { name: 'Somnath', value: 35, color: '#EA6E3C' },
  { name: 'Dwarkadhish', value: 28, color: '#4C3A7F' },
  { name: 'Ramnath', value: 22, color: '#10B981' },
  { name: 'Shreenathji', value: 15, color: '#F59E0B' },
];

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-blue-50/30 to-background">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button asChild variant="ghost" size="sm">
              <Link href="/" className="gap-2">
                <ArrowLeft className="w-4 h-4" />
                Back
              </Link>
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Live Monitoring Dashboard</h1>
              <p className="text-sm text-foreground/60">Real-time crowd analysis & risk assessment</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-green-600 font-medium">Live</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-foreground/60 mb-2">Current Crowd</p>
                <p className="text-3xl font-bold text-primary">24.5K</p>
                <p className="text-xs text-foreground/50 mt-2">+2.3% from last hour</p>
              </div>
              <Users className="w-10 h-10 text-primary/20" />
            </div>
          </Card>

          <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-foreground/60 mb-2">Risk Index</p>
                <p className="text-3xl font-bold text-orange-500">⚠️ Warning</p>
                <p className="text-xs text-foreground/50 mt-2">Approaching threshold</p>
              </div>
              <AlertTriangle className="w-10 h-10 text-orange-500/20" />
            </div>
          </Card>

          <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-foreground/60 mb-2">Next Hour Surge</p>
                <p className="text-3xl font-bold text-secondary">+15%</p>
                <p className="text-xs text-foreground/50 mt-2">Predicted increase</p>
              </div>
              <TrendingUp className="w-10 h-10 text-secondary/20" />
            </div>
          </Card>

          <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-foreground/60 mb-2">Response Time</p>
                <p className="text-3xl font-bold text-emerald-500">0.24s</p>
                <p className="text-xs text-foreground/50 mt-2">Avg prediction speed</p>
              </div>
              <Clock className="w-10 h-10 text-emerald-500/20" />
            </div>
          </Card>
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          {/* Main Chart */}
          <Card className="lg:col-span-2 bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-foreground mb-6">24-Hour Crowd Trend & Prediction</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={crowdData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="time" stroke="#6b7280" style={{ fontSize: '12px' }} />
                <YAxis stroke="#6b7280" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#fff', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="crowd" 
                  stroke="#EA6E3C" 
                  strokeWidth={3}
                  dot={{ fill: '#EA6E3C', r: 4 }}
                  name="Actual Crowd"
                />
                <Line 
                  type="monotone" 
                  dataKey="prediction" 
                  stroke="#4C3A7F" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={{ fill: '#4C3A7F', r: 3 }}
                  name="AI Prediction"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Risk Distribution */}
          <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6">
            <h2 className="text-lg font-semibold text-foreground mb-6">Risk Distribution by Temple</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={templeMetrics}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name} ${value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {templeMetrics.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Temple Status */}
        <Card className="bg-white/50 backdrop-blur-sm border border-white/60 rounded-2xl p-6 mb-8">
          <h2 className="text-lg font-semibold text-foreground mb-6">Temple Status Overview</h2>
          <div className="space-y-3">
            {[
              { name: 'Somnath Temple', crowd: '8.2K', risk: 'Critical', capacity: 85 },
              { name: 'Dwarkadhish Temple', crowd: '6.8K', risk: 'Warning', capacity: 68 },
              { name: 'Ramnath Temple', crowd: '5.1K', risk: 'Safe', capacity: 51 },
              { name: 'Shreenathji Temple', crowd: '4.4K', risk: 'Safe', capacity: 44 }
            ].map((temple, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-gradient-to-r from-white/20 to-white/10 rounded-xl border border-white/40 hover:border-white/60 transition">
                <div className="flex-1">
                  <p className="font-semibold text-foreground">{temple.name}</p>
                  <p className="text-sm text-foreground/60">{temple.crowd} devotees</p>
                </div>
                <div className="flex items-center gap-6">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all ${
                        temple.risk === 'Critical' ? 'bg-red-500' :
                        temple.risk === 'Warning' ? 'bg-orange-500' :
                        'bg-emerald-500'
                      }`}
                      style={{ width: `${temple.capacity}%` }}
                    ></div>
                  </div>
                  <div className="w-20 text-right">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                      temple.risk === 'Critical' ? 'bg-red-100 text-red-700' :
                      temple.risk === 'Warning' ? 'bg-orange-100 text-orange-700' :
                      'bg-emerald-100 text-emerald-700'
                    }`}>
                      {temple.risk}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Navigation Links */}
        <div className="grid md:grid-cols-3 gap-4">
          <Button asChild className="bg-primary hover:bg-primary/90 h-12 rounded-xl font-semibold">
            <Link href="/analytics">View Analytics →</Link>
          </Button>
          <Button asChild className="bg-secondary hover:bg-secondary/90 h-12 rounded-xl font-semibold text-white">
            <Link href="/alerts">Risk Alerts →</Link>
          </Button>
          <Button asChild variant="outline" className="h-12 rounded-xl font-semibold">
            <Link href="/temple-insights">Temple Insights →</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
