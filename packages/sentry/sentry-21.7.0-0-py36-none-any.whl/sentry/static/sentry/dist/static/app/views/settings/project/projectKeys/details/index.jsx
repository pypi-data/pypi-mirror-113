Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var keySettings_1 = tslib_1.__importDefault(require("app/views/settings/project/projectKeys/details/keySettings"));
var keyStats_1 = tslib_1.__importDefault(require("app/views/settings/project/projectKeys/details/keyStats"));
var ProjectKeyDetails = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectKeyDetails, _super);
    function ProjectKeyDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            react_router_1.browserHistory.push("/" + orgId + "/" + projectId + "/settings/keys/");
        };
        return _this;
    }
    ProjectKeyDetails.prototype.getTitle = function () {
        return locale_1.t('Key Details');
    };
    ProjectKeyDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
        return [['data', "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/"]];
    };
    ProjectKeyDetails.prototype.renderBody = function () {
        var data = this.state.data;
        var params = this.props.params;
        return (<div data-test-id="key-details">
        <settingsPageHeader_1.default title={locale_1.t('Key Details')}/>
        <permissionAlert_1.default />

        <keyStats_1.default api={this.api} params={params}/>

        <keySettings_1.default api={this.api} params={params} data={data} onRemove={this.handleRemove}/>
      </div>);
    };
    return ProjectKeyDetails;
}(asyncView_1.default));
exports.default = ProjectKeyDetails;
//# sourceMappingURL=index.jsx.map