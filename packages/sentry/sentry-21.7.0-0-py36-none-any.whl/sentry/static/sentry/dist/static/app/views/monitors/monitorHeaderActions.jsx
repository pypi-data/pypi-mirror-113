Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var logging_1 = require("app/utils/logging");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var MonitorHeaderActions = function (_a) {
    var api = _a.api, monitor = _a.monitor, orgId = _a.orgId, onUpdate = _a.onUpdate;
    var handleDelete = function () {
        var redirectPath = "/organizations/" + orgId + "/monitors/";
        indicator_1.addLoadingMessage(locale_1.t('Deleting Monitor...'));
        api
            .requestPromise("/monitors/" + monitor.id + "/", {
            method: 'DELETE',
        })
            .then(function () {
            react_router_1.browserHistory.push(redirectPath);
        })
            .catch(function () {
            indicator_1.addErrorMessage(locale_1.t('Unable to remove monitor.'));
        });
    };
    var updateMonitor = function (data) {
        indicator_1.addLoadingMessage();
        api
            .requestPromise("/monitors/" + monitor.id + "/", {
            method: 'PUT',
            data: data,
        })
            .then(function (resp) {
            indicator_1.clearIndicators();
            onUpdate === null || onUpdate === void 0 ? void 0 : onUpdate(resp);
        })
            .catch(function (err) {
            logging_1.logException(err);
            indicator_1.addErrorMessage(locale_1.t('Unable to update monitor.'));
        });
    };
    var toggleStatus = function () {
        return updateMonitor({
            status: monitor.status === 'disabled' ? 'active' : 'disabled',
        });
    };
    return (<ButtonContainer>
      <buttonBar_1.default gap={1}>
        <button_1.default size="small" icon={<icons_1.IconEdit size="xs"/>} to={"/organizations/" + orgId + "/monitors/" + monitor.id + "/edit/"}>
          &nbsp;
          {locale_1.t('Edit')}
        </button_1.default>
        <button_1.default size="small" onClick={toggleStatus}>
          {monitor.status !== 'disabled' ? locale_1.t('Pause') : locale_1.t('Enable')}
        </button_1.default>
        <confirm_1.default onConfirm={handleDelete} message={locale_1.t('Deleting this monitor is permanent. Are you sure you wish to continue?')}>
          <button_1.default size="small" icon={<icons_1.IconDelete size="xs"/>}>
            {locale_1.t('Delete')}
          </button_1.default>
        </confirm_1.default>
      </buttonBar_1.default>
    </ButtonContainer>);
};
var ButtonContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  display: flex;\n  flex-shrink: 1;\n"], ["\n  margin-bottom: ", ";\n  display: flex;\n  flex-shrink: 1;\n"])), space_1.default(3));
exports.default = withApi_1.default(MonitorHeaderActions);
var templateObject_1;
//# sourceMappingURL=monitorHeaderActions.jsx.map