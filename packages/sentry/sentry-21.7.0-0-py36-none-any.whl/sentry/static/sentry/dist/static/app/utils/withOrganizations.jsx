Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var organizationsStore_1 = tslib_1.__importDefault(require("app/stores/organizationsStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
function withOrganizations(WrappedComponent) {
    var WithOrganizations = /** @class */ (function (_super) {
        tslib_1.__extends(WithOrganizations, _super);
        function WithOrganizations() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { organizations: organizationsStore_1.default.getAll() };
            _this.unsubscribe = organizationsStore_1.default.listen(function (organizations) { return _this.setState({ organizations: organizations }); }, undefined);
            return _this;
        }
        WithOrganizations.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithOrganizations.prototype.render = function () {
            var _a = this.props, organizationsLoading = _a.organizationsLoading, organizations = _a.organizations, props = tslib_1.__rest(_a, ["organizationsLoading", "organizations"]);
            return (<WrappedComponent {...tslib_1.__assign({ organizationsLoading: organizationsLoading !== null && organizationsLoading !== void 0 ? organizationsLoading : !organizationsStore_1.default.loaded, organizations: organizations !== null && organizations !== void 0 ? organizations : this.state.organizations }, props)}/>);
        };
        WithOrganizations.displayName = "withOrganizations(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithOrganizations;
    }(React.Component));
    return WithOrganizations;
}
exports.default = withOrganizations;
//# sourceMappingURL=withOrganizations.jsx.map