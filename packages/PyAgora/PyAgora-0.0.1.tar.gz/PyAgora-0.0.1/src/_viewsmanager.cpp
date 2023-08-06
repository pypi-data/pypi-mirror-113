#include "_viewsmanager.h"

CViewsManager::CViewsManager()
{
}


CViewsManager::~CViewsManager()
{
}

CViewsManager *CViewsManager::getInstance()
{
    static CViewsManager cViewsManager;
	return &cViewsManager;
}

void CViewsManager::AddView(void* hWnd)
{
	m_wnds.push_back(hWnd);
	auto pos = find(m_wndFreeView.begin(), m_wndFreeView.end(), hWnd);
	if (pos != m_wndFreeView.end())
		return;

	m_wndFreeView.push_back(hWnd);
}

void CViewsManager::RemoveView(void* hView)
{
	m_wndFreeView.remove(hView);
}

void CViewsManager::FreeView(void* hView)
{
	auto pos = find(m_wndBusyView.begin(), m_wndBusyView.end(), hView);
	if (pos == m_wndBusyView.end())
		return;

	m_wndBusyView.remove(hView);
	m_wndFreeView.push_front(hView);
}

void CViewsManager::FreeAllView()
{
	m_wndFreeView.clear();
	//m_wndFreeView.AddTail(&m_wndBusyView);
	m_wndBusyView.clear();
	for (int i = 0; i < m_wnds.size(); i++){
		m_wndFreeView.push_back(m_wnds[i]); 
	}
}

void* CViewsManager::GetOneFreeView()
{
	if (m_wndFreeView.empty())
	{
		return nullptr;
	}
	void* res = m_wndFreeView.front();
	m_wndFreeView.pop_front();
	m_wndBusyView.push_back(res);

	return  res;
}

void* CViewsManager::GetFirstView()
{
    if(m_wnds.empty())
        return NULL;
	auto pos = find(m_wndFreeView.begin(), m_wndFreeView.end(), m_wnds[0]);
	if (pos == m_wndFreeView.end())
		return m_wnds[0];

	m_wndFreeView.remove(m_wnds[0]);
	m_wndBusyView.push_back(m_wnds[0]);

	return  m_wnds[0];
}

void* CViewsManager::GetViewAt(int i)
{
	if (i >= m_wnds.size())
		return NULL;

	return m_wnds[i];
}
