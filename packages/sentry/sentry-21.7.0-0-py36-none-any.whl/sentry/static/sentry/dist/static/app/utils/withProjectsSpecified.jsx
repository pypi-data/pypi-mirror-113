Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
/**
 * Higher order component that takes specificProjectSlugs and provides list of that projects from ProjectsStore
 */
function withProjectsSpecified(WrappedComponent) {
    var WithProjectsSpecified = /** @class */ (function (_super) {
        tslib_1.__extends(WithProjectsSpecified, _super);
        function WithProjectsSpecified() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = projectsStore_1.default.getState(_this.props.specificProjectSlugs);
            _this.unsubscribe = projectsStore_1.default.listen(function () {
                var storeState = projectsStore_1.default.getState(_this.props.specificProjectSlugs);
                if (!isEqual_1.default(_this.state, storeState)) {
                    _this.setState(storeState);
                }
            }, undefined);
            return _this;
        }
        WithProjectsSpecified.getDerivedStateFromProps = function (nextProps) {
            return projectsStore_1.default.getState(nextProps.specificProjectSlugs);
        };
        WithProjectsSpecified.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjectsSpecified.prototype.render = function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        };
        WithProjectsSpecified.displayName = "withProjectsSpecified(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithProjectsSpecified;
    }(React.Component));
    return WithProjectsSpecified;
}
exports.default = withProjectsSpecified;
//# sourceMappingURL=withProjectsSpecified.jsx.map