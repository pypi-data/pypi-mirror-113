Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var integrationExternalMappingForm_1 = tslib_1.__importDefault(require("app/components/integrationExternalMappingForm"));
var integrationExternalMappings_1 = tslib_1.__importDefault(require("app/components/integrationExternalMappings"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var IntegrationExternalUserMappings = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationExternalUserMappings, _super);
    function IntegrationExternalUserMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (mapping) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var organization, endpoint, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        endpoint = "/organizations/" + organization.slug + "/external-users/" + mapping.id + "/";
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        // remove config and update state
                        indicator_1.addSuccessMessage(locale_1.t('Deletion successful'));
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        // no 4xx errors should happen on delete
                        indicator_1.addErrorMessage(locale_1.t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function () {
            // Don't bother updating state. The info is in array of objects for each object in another array of objects.
            // Easier and less error-prone to re-fetch the data and re-calculate state.
            _this.fetchData();
        };
        _this.openModal = function (mapping) {
            var _a = _this.props, organization = _a.organization, integration = _a.integration;
            modal_1.openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Configure External User Mapping')}</Header>
        <Body>
          <integrationExternalMappingForm_1.default organization={organization} integration={integration} onSubmitSuccess={function () {
                        _this.handleSubmitSuccess();
                        closeModal();
                    }} mapping={mapping} sentryNamesMapper={_this.sentryNamesMapper} type="user" url={"/organizations/" + organization.slug + "/members/"} onCancel={closeModal} baseEndpoint={"/organizations/" + organization.slug + "/external-users/"}/>
        </Body>
      </react_1.Fragment>);
            });
        };
        return _this;
    }
    IntegrationExternalUserMappings.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [
            [
                'members',
                "/organizations/" + organization.slug + "/members/",
                { query: { query: 'hasExternalUsers:true', expand: 'externalUsers' } },
            ],
        ];
    };
    Object.defineProperty(IntegrationExternalUserMappings.prototype, "mappings", {
        get: function () {
            var integration = this.props.integration;
            var members = this.state.members;
            var externalUserMappings = members.reduce(function (acc, member) {
                var externalUsers = member.externalUsers, user = member.user;
                acc.push.apply(acc, tslib_1.__spreadArray([], tslib_1.__read(externalUsers
                    .filter(function (externalUser) { return externalUser.provider === integration.provider.key; })
                    .map(function (externalUser) { return (tslib_1.__assign(tslib_1.__assign({}, externalUser), { sentryName: user.name })); }))));
                return acc;
            }, []);
            return externalUserMappings.sort(function (a, b) { return parseInt(a.id, 10) - parseInt(b.id, 10); });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationExternalUserMappings.prototype.sentryNamesMapper = function (members) {
        return members
            .filter(function (member) { return member.user; })
            .map(function (_a) {
            var id = _a.user.id, email = _a.email, name = _a.name;
            var label = email !== name ? name + " - " + email : "" + email;
            return { id: id, name: label };
        });
    };
    IntegrationExternalUserMappings.prototype.renderBody = function () {
        var integration = this.props.integration;
        return (<react_1.Fragment>
        <integrationExternalMappings_1.default integration={integration} type="user" mappings={this.mappings} onCreateOrEdit={this.openModal} onDelete={this.handleDelete}/>
      </react_1.Fragment>);
    };
    return IntegrationExternalUserMappings;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(IntegrationExternalUserMappings);
//# sourceMappingURL=integrationExternalUserMappings.jsx.map