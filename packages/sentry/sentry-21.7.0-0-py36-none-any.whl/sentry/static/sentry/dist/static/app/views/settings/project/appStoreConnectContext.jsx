Object.defineProperty(exports, "__esModule", { value: true });
exports.Consumer = exports.Provider = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
var AppStoreConnectContext = react_1.createContext(undefined);
var Provider = withApi_1.default(withProject_1.default(function (_a) {
    var api = _a.api, children = _a.children, project = _a.project, orgSlug = _a.orgSlug;
    var _b = tslib_1.__read(react_1.useState(), 2), appStoreConnectValidationData = _b[0], setAppStoreConnectValidationData = _b[1];
    react_1.useEffect(function () {
        fetchAppStoreConnectValidationData();
    }, [project]);
    function getAppStoreConnectSymbolSourceId() {
        var _a;
        return (_a = (project.symbolSources ? JSON.parse(project.symbolSources) : []).find(function (symbolSource) { return symbolSource.type.toLowerCase() === 'appstoreconnect'; })) === null || _a === void 0 ? void 0 : _a.id;
    }
    function fetchAppStoreConnectValidationData() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var appStoreConnectSymbolSourceId, response, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        appStoreConnectSymbolSourceId = getAppStoreConnectSymbolSourceId();
                        if (!appStoreConnectSymbolSourceId) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + project.slug + "/appstoreconnect/validate/" + appStoreConnectSymbolSourceId + "/")];
                    case 2:
                        response = _b.sent();
                        setAppStoreConnectValidationData(tslib_1.__assign({ id: appStoreConnectSymbolSourceId }, response));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    return (<AppStoreConnectContext.Provider value={appStoreConnectValidationData}>
        {children}
      </AppStoreConnectContext.Provider>);
}));
exports.Provider = Provider;
var Consumer = AppStoreConnectContext.Consumer;
exports.Consumer = Consumer;
exports.default = AppStoreConnectContext;
//# sourceMappingURL=appStoreConnectContext.jsx.map