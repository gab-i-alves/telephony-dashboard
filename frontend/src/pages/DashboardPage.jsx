import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import apiClient from "../services/api";
import KpiCard from "../components/KpiCard";
import CallsTable from "../components/CallsTable";
import Pagination from "../components/Pagination";
import CallsChart from "../components/CallsChart";

const DashboardPage = () => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const [kpis, setKpis] = useState(null);
  const [kpisLoading, setKpisLoading] = useState(true);
  const [kpisError, setKpisError] = useState(null);

  const [calls, setCalls] = useState([]);
  const [callsLoading, setCallsLoading] = useState(true);
  const [callsError, setCallsError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [chartData, setChartData] = useState([]);
  const [chartLoading, setChartLoading] = useState(true);
  const [chartError, setChartError] = useState(null);

  useEffect(() => {
    const fetchKpis = async () => {
      try {
        setKpisLoading(true);
        const response = await apiClient.get("/metrics/kpis");
        setKpis(response.data);
      } catch (err) {
        setKpisError("Não foi possível carregar os KPIs.");
      } finally {
        setKpisLoading(false);
      }
    };
    fetchKpis();
  }, []);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        setChartLoading(true);
        const response = await apiClient.get("/metrics/calls_by_hour");
        setChartData(response.data);
      } catch (err) {
        setChartError("Não foi possível carregar os dados do gráfico.");
      } finally {
        setChartLoading(false);
      }
    };
    fetchChartData();
  }, []);

  useEffect(() => {
    const fetchCalls = async () => {
      try {
        setCallsLoading(true);
        const response = await apiClient.get(
          `/calls?page=${currentPage}&limit=10`
        );
        setCalls(response.data.data);
        setTotalPages(Math.ceil(response.data.total / response.data.limit));
      } catch (err) {
        setCallsError("Não foi possível carregar os detalhes das chamadas.");
      } finally {
        setCallsLoading(false);
      }
    };
    fetchCalls();
  }, [currentPage]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const renderKpiContent = () => {
    if (kpisLoading) {
      return <p>A carregar KPIs...</p>;
    }
    if (kpisError) {
      return <p className="text-red-500">{kpisError}</p>;
    }
    if (kpis) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard title="Total de Chamadas" value={kpis.total_calls} />
          <KpiCard title="Chamadas Atendidas" value={kpis.answered_calls} />
          <KpiCard
            title="ASR (Taxa de Atendimento)"
            value={kpis.asr}
            unit="%"
          />
          <KpiCard title="ACD (Duração Média)" value={kpis.acd} unit="s" />
        </div>
      );
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white">
      <nav className="bg-white dark:bg-gray-800 shadow-md p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">Dashboard de Telefonia</h1>
        <div>
          <span className="mr-4">Olá, {user?.email}</span>
          <button
            onClick={handleLogout}
            className="px-4 py-2 font-semibold text-white bg-red-600 rounded hover:bg-red-700"
          >
            Sair
          </button>
        </div>
      </nav>

      <main className="p-8">
        <h2 className="text-2xl mb-6">Métricas Gerais</h2>
        {renderKpiContent()}

        <div className="mt-8">
          <h2 className="text-2xl mb-6">Volume de Chamadas por Hora</h2>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <CallsChart
              data={chartData}
              isLoading={chartLoading}
              error={chartError}
            />
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-2xl mb-6">Detalhes das Chamadas</h2>
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
            <CallsTable
              calls={calls}
              isLoading={callsLoading}
              error={callsError}
            />
            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
