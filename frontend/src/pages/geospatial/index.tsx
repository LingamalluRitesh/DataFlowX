import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { MapPin, Navigation, Globe, CheckCircle, Compass, Layers } from 'lucide-react';

interface GeoLocationItem {
  location_id: string;
  name: string;
  latitude: number;
  longitude: number;
  distance_from_hq_km: number;
  geohash_prefix: string;
  bounding_box_match: boolean;
}

const mockLocations: GeoLocationItem[] = [
  { location_id: 'loc_01', name: 'New York Data Center', latitude: 40.7128, longitude: -74.0060, distance_from_hq_km: 12.4, geohash_prefix: 'dr5reg', bounding_box_match: true },
  { location_id: 'loc_02', name: 'London Cloud Region', latitude: 51.5074, longitude: -0.1278, distance_from_hq_km: 5567.0, geohash_prefix: 'gcpvj0', bounding_box_match: false },
  { location_id: 'loc_03', name: 'San Francisco Hub', latitude: 37.7749, longitude: -122.4194, distance_from_hq_km: 4128.5, geohash_prefix: '9q8yyk', bounding_box_match: false },
];

export default function GeospatialStudioPage() {
  const columns: DataGridColumn<GeoLocationItem>[] = [
    {
      key: 'name',
      header: 'Geographic Asset',
      render: (g) => (
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-cyan-400" />
          <div>
            <strong className="text-white text-xs">{g.name}</strong>
            <div className="text-[10px] text-slate-500 font-mono">{g.location_id}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'latitude',
      header: 'GPS Coordinates (Lat / Lon)',
      render: (g) => (
        <span className="font-mono text-xs text-slate-300">
          {g.latitude.toFixed(4)}, {g.longitude.toFixed(4)}
        </span>
      ),
    },
    { key: 'geohash_prefix', header: 'Geohash Level-6', render: (g) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{g.geohash_prefix}</span> },
    {
      key: 'distance_from_hq_km',
      header: 'Haversine Distance',
      render: (g) => <span className="font-mono text-emerald-400 font-bold">{g.distance_from_hq_km.toLocaleString()} km</span>,
    },
    {
      key: 'bounding_box_match',
      header: 'Spatial Bounding Filter',
      render: (g) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            g.bounding_box_match
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {g.bounding_box_match ? 'INSIDE BOUNDS' : 'OUTSIDE'}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Geospatial & Spatial Indexing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Globe className="w-7 h-7 text-cyan-400" />
            Geospatial Calculations & Spatial Indexing Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Vectorized spherical Haversine distances, Geohash spatial prefixes, and bounding-box spatial containment filters.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Indexed Spatial Coordinates</div>
            <div className="text-2xl font-bold text-white mt-1">3 Locations</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Distance Calculation Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">12.5M pairs / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Spatial Indexing Model</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Geohash + R-Tree</div>
          </div>
        </div>

        <DataGrid data={mockLocations} columns={columns} title="Geospatial Assets & Distances" />
      </div>
    </MainLayout>
  );
}
