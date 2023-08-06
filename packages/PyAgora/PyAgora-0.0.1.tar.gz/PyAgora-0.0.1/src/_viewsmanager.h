#pragma once

#include <list>
#include <vector>

using namespace std;
class CViewsManager
{
protected:
	CViewsManager();
	~CViewsManager();

public:
	void AddView(void* hWnd);
	void RemoveView(void* hView);
	void FreeView(void* hView);
	void FreeAllView();
	void* GetOneFreeView();
	void* GetFirstView();
	void* GetViewAt(int i);

public:
	static CViewsManager *getInstance();    
private:
	list<void*>		m_wndFreeView;
	list<void*>		m_wndBusyView;
	vector<void*>      m_wnds;
};

