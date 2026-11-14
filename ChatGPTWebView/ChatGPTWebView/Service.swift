import Foundation

struct InjectedJavaScript {
    let documentStart: String?
    let documentEnd: String?
    let didFinish: String?
}

enum Service: CaseIterable {
    case chatgpt

    var homeURL: URL {
        if let local = Bundle.main.url(forResource: "index", withExtension: "html") {
            return local
        }
        return URL(string: "about:blank")!
    }

    var title: String {
        "诗鉴"
    }

    var tabIconSystemName: String {
        "sparkles"
    }

    var userAgentOverride: String? {
        nil
    }

    var injectedJavaScript: InjectedJavaScript? {
        nil
    }

    var zoomDefaultsKey: String {
        "zoomScale.shijian"
    }

    var websiteDataDomain: String {
        "localhost"
    }
}
