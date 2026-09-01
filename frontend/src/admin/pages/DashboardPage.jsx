import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { adminApi } from '../services/api';

export const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [visitTrend, setVisitTrend] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    Promise.all([
      adminApi.getDashboardStats(),
      adminApi.getVisitTrend(7),
    ]).then(([statsData, trendData]) => {
      setStats(statsData);
      setVisitTrend(trendData.trend || []);
    }).finally(() => {
      setLoading(false);
    });
  };

  const statCards = [
    { label: '植物总数', value: stats?.total_plants || 0, icon: '🌿', color: 'from-green-400 to-emerald-600', bgColor: 'bg-green-50' },
    { label: '植物科属', value: stats?.families_count || 0, icon: '📚', color: 'from-blue-400 to-indigo-600', bgColor: 'bg-blue-50' },
    { label: '受保护植物', value: stats?.protected_count || 0, icon: '🛡️', color: 'from-amber-400 to-orange-600', bgColor: 'bg-amber-50' },
    { label: '分布区域', value: stats?.zones_count || 0, icon: '🗺️', color: 'from-pink-400 to-rose-600', bgColor: 'bg-pink-50' },
  ];

  const visitCards = [
    { label: '今日访问', value: stats?.today_visits || 0, icon: '📅' },
    { label: '本周访问', value: stats?.weekly_visits || 0, icon: '📆' },
    { label: '总访问量', value: stats?.total_visits || 0, icon: '👁️' },
  ];

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">仪表盘</h1>
          <p className="text-gray-500">欢迎回来，查看系统概览</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {statCards.map((card, index) => (
            <div
              key={index}
              className={`${card.bgColor} rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-lg`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">{card.label}</p>
                  <p className="text-3xl font-bold text-gray-800">{card.value}</p>
                </div>
                <div className={`w-14 h-14 bg-gradient-to-br ${card.color} rounded-xl flex items-center justify-center shadow-lg`}>
                  <span className="text-2xl">{card.icon}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {visitCards.map((card, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow duration-300"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
                  <span className="text-xl">{card.icon}</span>
                </div>
                <div>
                  <p className="text-gray-500 text-sm">{card.label}</p>
                  <p className="text-2xl font-bold text-gray-800">{card.value}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-gray-800 mb-6">访问趋势</h2>
          <div className="h-64">
            <div className="flex items-end justify-between h-full gap-4">
              {visitTrend.map((item, index) => {
                const maxCount = Math.max(...visitTrend.map(t => t.count), 1);
                const height = (item.count / maxCount) * 100;
                return (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div className="w-full flex-1 flex items-end">
                      <div
                        className="w-full bg-gradient-to-t from-green-500 to-emerald-400 rounded-t-lg transition-all duration-500"
                        style={{ height: `${Math.max(height, 5)}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-2">
                      {item.date ? item.date.split('-').slice(1).join('/') : ''}
                    </p>
                    <p className="text-sm font-semibold text-gray-700">{item.count}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};
