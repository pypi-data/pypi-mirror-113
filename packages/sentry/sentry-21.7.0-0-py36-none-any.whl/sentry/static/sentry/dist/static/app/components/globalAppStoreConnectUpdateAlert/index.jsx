Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var AppStoreConnectContext = tslib_1.__importStar(require("app/components/projects/appStoreConnectContext"));
var updateAlert_1 = tslib_1.__importDefault(require("./updateAlert"));
function GlobalAppStoreConnectUpdateAlert(_a) {
    var project = _a.project, organization = _a.organization, rest = tslib_1.__rest(_a, ["project", "organization"]);
    return (<AppStoreConnectContext.Provider project={project} organization={organization}>
      <updateAlert_1.default project={project} organization={organization} {...rest}/>
    </AppStoreConnectContext.Provider>);
}
exports.default = GlobalAppStoreConnectUpdateAlert;
//# sourceMappingURL=index.jsx.map