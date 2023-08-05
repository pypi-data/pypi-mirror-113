Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("app/utils/handleXhrErrorResponse"));
var marked_1 = tslib_1.__importDefault(require("app/utils/marked"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var utils_1 = require("./utils");
function UpgradeGrouping(_a) {
    var _this = this;
    var groupingConfigs = _a.groupingConfigs, organization = _a.organization, projectId = _a.projectId, project = _a.project, onUpgrade = _a.onUpgrade, api = _a.api;
    var hasAccess = organization.access.includes('project:write');
    var _b = utils_1.getGroupingChanges(project, groupingConfigs), updateNotes = _b.updateNotes, riskLevel = _b.riskLevel, latestGroupingConfig = _b.latestGroupingConfig;
    var _c = utils_1.getGroupingRisk(riskLevel), riskNote = _c.riskNote, alertType = _c.alertType;
    var noUpdates = !latestGroupingConfig;
    var newData = {};
    if (latestGroupingConfig) {
        newData.groupingConfig = latestGroupingConfig.id;
    }
    var handleUpgrade = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var response, _a;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    indicator_1.addLoadingMessage(locale_1.t('Changing grouping\u2026'));
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/", {
                            method: 'PUT',
                            data: newData,
                        })];
                case 2:
                    response = _b.sent();
                    indicator_1.clearIndicators();
                    projectActions_1.default.updateSuccess(response);
                    onUpgrade();
                    return [3 /*break*/, 4];
                case 3:
                    _a = _b.sent();
                    handleXhrErrorResponse_1.default(locale_1.t('Unable to upgrade config'));
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    if (!groupingConfigs) {
        return null;
    }
    function getModalMessage() {
        return (<react_1.Fragment>
        <textBlock_1.default>
          <strong>{locale_1.t('Upgrade Grouping Strategy')}</strong>
        </textBlock_1.default>
        <textBlock_1.default>
          {locale_1.t('You can upgrade the grouping strategy to the latest but this is an irreversible operation.')}
        </textBlock_1.default>
        <textBlock_1.default>
          <strong>{locale_1.t('New Behavior')}</strong>
          <div dangerouslySetInnerHTML={{ __html: marked_1.default(updateNotes) }}/>
        </textBlock_1.default>
        <textBlock_1.default>
          <alert_1.default type={alertType}>{riskNote}</alert_1.default>
        </textBlock_1.default>
      </react_1.Fragment>);
    }
    function getButtonTitle() {
        if (!hasAccess) {
            return locale_1.t('You do not have sufficient permissions to do this');
        }
        if (noUpdates) {
            return locale_1.t('You are already on the latest version');
        }
        return undefined;
    }
    return (<panels_1.Panel id="upgrade-grouping">
      <panels_1.PanelHeader>{locale_1.t('Upgrade Grouping')}</panels_1.PanelHeader>
      <panels_1.PanelBody>
        <field_1.default label={locale_1.t('Upgrade Grouping Strategy')} help={locale_1.tct('If the project uses an old grouping strategy an update is possible.[linebreak]Doing so will cause new events to group differently.', {
            linebreak: <br />,
        })} disabled>
          <confirm_1.default disabled={noUpdates} onConfirm={handleUpgrade} priority={riskLevel >= 2 ? 'danger' : 'primary'} confirmText={locale_1.t('Upgrade')} message={getModalMessage()}>
            <div>
              <button_1.default disabled={!hasAccess || noUpdates} title={getButtonTitle()} type="button" priority={riskLevel >= 2 ? 'danger' : 'primary'}>
                {locale_1.t('Upgrade Grouping Strategy')}
              </button_1.default>
            </div>
          </confirm_1.default>
        </field_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = UpgradeGrouping;
//# sourceMappingURL=upgradeGrouping.jsx.map