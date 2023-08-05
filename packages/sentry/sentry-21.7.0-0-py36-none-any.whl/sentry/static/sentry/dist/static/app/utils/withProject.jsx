Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Currently wraps component with project from context
 */
var withProject = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        tslib_1.__extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _a = this.props, project = _a.project, props = tslib_1.__rest(_a, ["project"]);
            return (<WrappedComponent {...tslib_1.__assign({ project: project !== null && project !== void 0 ? project : this.context.project }, props)}/>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withProject(" + getDisplayName_1.default(WrappedComponent) + ")",
    _a.contextTypes = {
        project: sentryTypes_1.default.Project,
    },
    _a; };
exports.default = withProject;
//# sourceMappingURL=withProject.jsx.map