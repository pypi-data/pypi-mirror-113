Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var rulesPanel_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/rulesPanel"));
var CodeOwnersPanel = /** @class */ (function (_super) {
    tslib_1.__extends(CodeOwnersPanel, _super);
    function CodeOwnersPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (codeowner) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, project, onDelete, endpoint, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, onDelete = _a.onDelete;
                        endpoint = "/api/0/projects/" + organization.slug + "/" + project.slug + "/codeowners/" + codeowner.id + "/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _c.sent();
                        onDelete(codeowner);
                        indicator_1.addSuccessMessage(locale_1.t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        // no 4xx errors should happen on delete
                        indicator_1.addErrorMessage(locale_1.t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CodeOwnersPanel.prototype.render = function () {
        var _this = this;
        var codeowners = this.props.codeowners;
        return (codeowners || []).map(function (codeowner) {
            var dateUpdated = codeowner.dateUpdated, provider = codeowner.provider, repoName = codeowner.codeMapping.repoName, ownershipSyntax = codeowner.ownershipSyntax;
            return (<react_1.Fragment key={codeowner.id}>
          <rulesPanel_1.default data-test-id="codeowners-panel" type="codeowners" raw={ownershipSyntax} dateUpdated={dateUpdated} provider={provider} repoName={repoName} readOnly controls={[
                    <confirm_1.default onConfirm={function () { return _this.handleDelete(codeowner); }} message={locale_1.t('Are you sure you want to remove this CODEOWNERS file?')} key="confirm-delete">
                <button_1.default key="delete" icon={<icons_1.IconDelete size="xs"/>} size="xsmall"/>
              </confirm_1.default>,
                ]}/>
        </react_1.Fragment>);
        });
    };
    return CodeOwnersPanel;
}(react_1.Component));
exports.default = withApi_1.default(CodeOwnersPanel);
//# sourceMappingURL=codeowners.jsx.map