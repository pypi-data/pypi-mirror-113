Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var withProject_1 = tslib_1.__importDefault(require("app/utils/withProject"));
/**
 * Simple Component that takes project from context and passes it as props to children
 *
 * Don't do anything additional (e.g. loader) because not all children require project
 *
 * This is made because some components (e.g. ProjectPluginDetail) takes project as prop
 */
var SettingsProjectProvider = /** @class */ (function (_super) {
    tslib_1.__extends(SettingsProjectProvider, _super);
    function SettingsProjectProvider() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsProjectProvider.prototype.render = function () {
        var _a = this.props, children = _a.children, project = _a.project;
        if (react_1.isValidElement(children)) {
            return react_1.cloneElement(children, tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, this.props), children.props), { project: project }));
        }
        return null;
    };
    return SettingsProjectProvider;
}(react_1.Component));
exports.default = withProject_1.default(SettingsProjectProvider);
//# sourceMappingURL=settingsProjectProvider.jsx.map