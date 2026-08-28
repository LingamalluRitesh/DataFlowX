import type { AppProps } from 'next/app';
import { AuthProvider } from '@/context/AuthContext';
import { WorkspaceProvider } from '@/context/WorkspaceContext';
import { Layout } from '@/components/layout/Layout';
import '@/styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <WorkspaceProvider>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </WorkspaceProvider>
    </AuthProvider>
  );
}
