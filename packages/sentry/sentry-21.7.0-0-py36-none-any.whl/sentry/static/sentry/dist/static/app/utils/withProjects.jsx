Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses ProjectsStore and provides a list of projects
 */
function withProjects(WrappedComponent) {
    var WithProjects = /** @class */ (function (_super) {
        tslib_1.__extends(WithProjects, _super);
        function WithProjects() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = projectsStore_1.default.getState();
            _this.unsubscribe = projectsStore_1.default.listen(function () { return _this.setState(projectsStore_1.default.getState()); }, undefined);
            return _this;
        }
        WithProjects.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjects.prototype.render = function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        };
        WithProjects.displayName = "withProjects(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithProjects;
    }(React.Component));
    return WithProjects;
}
exports.default = withProjects;
//# sourceMappingURL=withProjects.jsx.map