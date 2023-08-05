Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var release_1 = require("app/actionCreators/release");
var releaseStore_1 = tslib_1.__importDefault(require("app/stores/releaseStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
function withRelease(WrappedComponent) {
    var WithRelease = /** @class */ (function (_super) {
        tslib_1.__extends(WithRelease, _super);
        function WithRelease(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribe = releaseStore_1.default.listen(function () { return _this.onStoreUpdate(); }, undefined);
            var _a = _this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            _this.state = tslib_1.__assign({}, releaseData);
            return _this;
        }
        WithRelease.prototype.componentDidMount = function () {
            this.fetchRelease();
            this.fetchDeploys();
        };
        WithRelease.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithRelease.prototype.fetchRelease = function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.release && !releaseData.releaseLoading) ||
                releaseData.releaseError) {
                release_1.getProjectRelease(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        };
        WithRelease.prototype.fetchDeploys = function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.deploys && !releaseData.deploysLoading) ||
                releaseData.deploysError) {
                release_1.getReleaseDeploys(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        };
        WithRelease.prototype.onStoreUpdate = function () {
            var _a = this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = releaseStore_1.default.get(projectSlug, releaseVersion);
            this.setState(tslib_1.__assign({}, releaseData));
        };
        WithRelease.prototype.render = function () {
            return (<WrappedComponent {...this.props} {...this.state}/>);
        };
        WithRelease.displayName = "withRelease(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithRelease;
    }(React.Component));
    return WithRelease;
}
exports.default = withRelease;
//# sourceMappingURL=withRelease.jsx.map