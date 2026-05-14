import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { adminApi } from '../services/api';

export const SpiderPage = () => {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const data = await adminApi.getSpiderConfig();
      setConfig(data);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      await adminApi.updateSpiderConfig(config);
      alert('配置已保存');
    } catch (err) {
      alert(err.message);
    }
  };

  const handleRunNow = async () => {
    if (!window.confirm('确定要立即执行爬虫吗？')) {
      return;
    }

    setRunning(true);
    try {
      await adminApi.runSpiderNow();
      alert('爬虫执行完成');
    } catch (err) {
      alert(err.message);
    } finally {
      setRunning(false);
    }
  };

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
      <div className="space-y-6 max-w-3xl">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">爬虫配置</h1>
          <p className="text-gray-500">配置数据爬取任务的执行策略</p>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm space-y-6">
          <div>
            <label 
              className="flex items-center justify-between p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors"
              onClick={() => setConfig({ ...config, enabled: !config.enabled })}
            >
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔄</span>
                <div>
                  <p className="font-medium text-gray-800">启用爬虫</p>
                  <p className="text-sm text-gray-500">开启后将按计划自动执行</p>
                </div>
              </div>
              <div className={`w-12 h-7 rounded-full transition-colors ${config.enabled ? 'bg-green-500' : 'bg-gray-300'}`}>
                <div
                  className={`w-5 h-5 bg-white rounded-full shadow-md transform transition-transform mt-1 ${config.enabled ? 'translate-x-6' : 'translate-x-1'}`}
                ></div>
              </div>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              执行频率
            </label>
            <div className="grid grid-cols-2 gap-3">
              {[
                { value: 'daily', label: '每天', desc: '每日固定时间执行' },
                { value: 'interval', label: '间隔', desc: '按时间间隔执行' },
              ].map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setConfig({ ...config, frequency_type: option.value })}
                  className={`p-4 rounded-xl border-2 text-left transition-all ${
                    config.frequency_type === option.value
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <p className="font-medium text-gray-800">{option.label}</p>
                  <p className="text-sm text-gray-500">{option.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {config.frequency_type === 'daily' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  执行时间 (小时)
                </label>
                <input
                  type="number"
                  min="0"
                  max="23"
                  value={config.cron_hour}
                  onChange={(e) => setConfig({ ...config, cron_hour: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  执行时间 (分钟)
                </label>
                <input
                  type="number"
                  min="0"
                  max="59"
                  value={config.cron_minute}
                  onChange={(e) => setConfig({ ...config, cron_minute: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
          )}

          {config.frequency_type === 'interval' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                执行间隔 (分钟)
              </label>
              <input
                type="number"
                min="1"
                value={config.interval_minutes}
                onChange={(e) => setConfig({ ...config, interval_minutes: parseInt(e.target.value) || 60 })}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              />
            </div>
          )}

          <div className="flex gap-4 pt-4">
            <button
              onClick={handleSave}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-xl shadow-lg shadow-green-200 hover:shadow-xl transition-all"
            >
              保存配置
            </button>
            <button
              onClick={handleRunNow}
              disabled={running}
              className="px-8 py-3 bg-gray-100 text-gray-700 font-medium rounded-xl hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {running ? '执行中...' : '立即执行'}
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
};
