const loadGoogleMaps = (apiKey, callbackName = "initMap") => {
  return new Promise((resolve, reject) => {
    // 检查是否已经加载过 Google Maps API
    if (window.google && window.google.maps) {
      resolve(window.google.maps);
      return;
    }

    // 创建 <script> 标签
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=${callbackName}`;
    script.async = true;
    script.defer = true;

    // 处理加载成功和失败的情况
    script.onload = () => resolve(window.google.maps);
    script.onerror = (err) => reject(err);

    // 添加到 <head>
    document.head.appendChild(script);
  });
};

export default loadGoogleMaps;