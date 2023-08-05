Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var organizationRepositories_1 = tslib_1.__importDefault(require("./organizationRepositories"));
var OrganizationRepositoriesContainer = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationRepositoriesContainer, _super);
    function OrganizationRepositoriesContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Callback used by child component to signal state change
        _this.onRepositoryChange = function (data) {
            var itemList = _this.state.itemList;
            itemList === null || itemList === void 0 ? void 0 : itemList.forEach(function (item) {
                if (item.id === data.id) {
                    item.status = data.status;
                }
            });
            _this.setState({ itemList: itemList });
        };
        return _this;
    }
    OrganizationRepositoriesContainer.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['itemList', "/organizations/" + orgId + "/repos/", { query: { status: '' } }]];
    };
    OrganizationRepositoriesContainer.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle_1.default(locale_1.t('Repositories'), orgId, false);
    };
    OrganizationRepositoriesContainer.prototype.renderBody = function () {
        var _a = this.state, itemList = _a.itemList, itemListPageLinks = _a.itemListPageLinks;
        return (<react_1.Fragment>
        <organizationRepositories_1.default {...this.props} itemList={itemList} api={this.api} onRepositoryChange={this.onRepositoryChange}/>
        {itemListPageLinks && (<pagination_1.default pageLinks={itemListPageLinks} {...this.props}/>)}
      </react_1.Fragment>);
    };
    return OrganizationRepositoriesContainer;
}(asyncView_1.default));
exports.default = OrganizationRepositoriesContainer;
//# sourceMappingURL=index.jsx.map