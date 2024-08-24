#include <vector>

class LocationManager {
 public:
    LocationManager();
    ~LocationManager();
};

// This is a comment
class V2xManager {
 public:
    V2xManager();
    ~V2xManager();

    int error_dump(int e);
    std::vector<long long> Loading();

    int start();
    void* sendBuffer();
 private:
    class ServiceStub : public LocationManager {
     public:
        explicit ServiceStub(V2xManager& parent) : m_parent(parent) {}
        virtual ~ServiceStub();
        virtual void Subscribe();
    
     private:
        V2xManager& m_parent;
    };
 private:
   void get_handler();
};