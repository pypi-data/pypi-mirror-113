Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var sdkUpdates_1 = require("app/actionCreators/sdkUpdates");
var sdkUpdatesStore_1 = tslib_1.__importDefault(require("app/stores/sdkUpdatesStore"));
var withApi_1 = tslib_1.__importDefault(require("./withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("./withOrganization"));
function withSdkUpdates(WrappedComponent) {
    var WithProjectSdkSuggestions = /** @class */ (function (_super) {
        tslib_1.__extends(WithProjectSdkSuggestions, _super);
        function WithProjectSdkSuggestions() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = { sdkUpdates: [] };
            _this.unsubscribe = sdkUpdatesStore_1.default.listen(function () { return _this.onSdkUpdatesUpdate(); }, undefined);
            return _this;
        }
        WithProjectSdkSuggestions.prototype.componentDidMount = function () {
            var orgSlug = this.props.organization.slug;
            var updates = sdkUpdatesStore_1.default.getUpdates(orgSlug);
            // Load SdkUpdates
            if (updates !== undefined) {
                this.onSdkUpdatesUpdate();
                return;
            }
            sdkUpdates_1.loadSdkUpdates(this.props.api, orgSlug);
        };
        WithProjectSdkSuggestions.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithProjectSdkSuggestions.prototype.onSdkUpdatesUpdate = function () {
            var _a;
            var sdkUpdates = (_a = sdkUpdatesStore_1.default.getUpdates(this.props.organization.slug)) !== null && _a !== void 0 ? _a : null;
            this.setState({ sdkUpdates: sdkUpdates });
        };
        WithProjectSdkSuggestions.prototype.render = function () {
            // TODO(ts) This unknown cast isn't great but Typescript complains about arbitrary
            // types being possible. I think this is related to the additional HoC wrappers causing type data to
            // be lost.
            return (<WrappedComponent {...this.props} sdkUpdates={this.state.sdkUpdates}/>);
        };
        return WithProjectSdkSuggestions;
    }(React.Component));
    return withOrganization_1.default(withApi_1.default(WithProjectSdkSuggestions));
}
exports.default = withSdkUpdates;
//# sourceMappingURL=withSdkUpdates.jsx.map