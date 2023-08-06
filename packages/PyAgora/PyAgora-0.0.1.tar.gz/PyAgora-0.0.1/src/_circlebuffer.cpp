
#include <iostream>
#include "_circlebuffer.h"

CircleBuffer* CircleBuffer::GetInstance()
{
	static CircleBuffer circleBuffer(MAX_AUDIO_SAMPLE_SIZE);
    return &circleBuffer;
}

void CircleBuffer::CloseInstance()
{
}

CircleBuffer::CircleBuffer(const unsigned int iBufferSize)
	:freeSpace(iBufferSize, iBufferSize),
	usedSpace(0, iBufferSize)
{
	this->m_iBufferSize = iBufferSize;
	this->m_pBuffer = (BYTE*)malloc(iBufferSize);
}

CircleBuffer::~CircleBuffer(void)
{
	free(this->m_pBuffer);
}

unsigned int CircleBuffer::getFreeSize()
{
	return freeSpace.getCount();
}

unsigned int CircleBuffer::getUsedSize()
{
	return usedSpace.getCount();
}


int CircleBuffer::writeBuffer(const void* pSourceBuffer, const unsigned int iNumBytes)
{
	if (iNumBytes > getFreeSize())
	{
		std::cout << "error iNumBytes: "<< iNumBytes <<" is greater than free buffer size" << std::endl;
		return 0;
	}
		
	unsigned int iBytesToWrite = iNumBytes;
	BYTE* pSourceReadCursor = (BYTE*)pSourceBuffer;

	auto cur = freeSpace.acquire(iNumBytes);

	unsigned int iChunkSize = this->m_iBufferSize - cur;
	if (iChunkSize > iBytesToWrite)
		iChunkSize = iBytesToWrite;

	memcpy(this->m_pBuffer + cur, pSourceReadCursor, iChunkSize);
	pSourceReadCursor += iChunkSize;
	iBytesToWrite -= iChunkSize;
	cur += iChunkSize;

	cur %= this->m_iBufferSize;

	if (iBytesToWrite)
	{
		memcpy(this->m_pBuffer + cur, pSourceReadCursor, iBytesToWrite);
	}

	usedSpace.release(iNumBytes);
    return iNumBytes;
}

int CircleBuffer::readBuffer(void* pDestBuffer, const unsigned int _iBytesToRead, unsigned int* pbBytesRead, int& audioTime)
{
	if (_iBytesToRead > getUsedSize() )
	{
		std::cout << "error _iBytesToRead: " << _iBytesToRead << " is greater than used buffer size" << std::endl;
		return 0;
	}

	unsigned int iBytesToRead = _iBytesToRead;
	unsigned int iBytesRead = 0;

	auto cur = usedSpace.acquire(_iBytesToRead);

	unsigned int iChunkSize = this->m_iBufferSize - cur;
	if (iChunkSize > iBytesToRead)
		iChunkSize = iBytesToRead;

	memcpy((BYTE*)pDestBuffer + iBytesRead, this->m_pBuffer + cur, iChunkSize);

	iBytesRead += iChunkSize;
	iBytesToRead -= iChunkSize;
	cur += iChunkSize;
	cur %= this->m_iBufferSize;

	if (iBytesToRead)
	{
		memcpy((BYTE*)pDestBuffer + iBytesRead, this->m_pBuffer + cur, iBytesToRead);
	}

	freeSpace.release(_iBytesToRead);
	
	*pbBytesRead = iBytesRead;
	return _iBytesToRead;
}

