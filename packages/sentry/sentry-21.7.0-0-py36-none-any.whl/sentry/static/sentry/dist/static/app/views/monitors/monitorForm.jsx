Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var mobx_react_1 = require("mobx-react");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var numberField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/numberField"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var monitorModel_1 = tslib_1.__importDefault(require("./monitorModel"));
var SCHEDULE_TYPES = [
    ['crontab', 'Crontab'],
    ['interval', 'Interval'],
];
var MONITOR_TYPES = [['cron_job', 'Cron Job']];
var INTERVALS = [
    ['minute', 'minute(s)'],
    ['hour', 'hour(s)'],
    ['day', 'day(s)'],
    ['week', 'week(s)'],
    ['month', 'month(s)'],
    ['year', 'year(s)'],
];
var MonitorForm = /** @class */ (function (_super) {
    tslib_1.__extends(MonitorForm, _super);
    function MonitorForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.form = new monitorModel_1.default();
        return _this;
    }
    MonitorForm.prototype.formDataFromConfig = function (type, config) {
        var rv = {};
        switch (type) {
            case 'cron_job':
                rv['config.schedule_type'] = config.schedule_type;
                rv['config.checkin_margin'] = config.checkin_margin;
                rv['config.max_runtime'] = config.max_runtime;
                switch (config.schedule_type) {
                    case 'interval':
                        rv['config.schedule.frequency'] = config.schedule[0];
                        rv['config.schedule.interval'] = config.schedule[1];
                        break;
                    case 'crontab':
                    default:
                        rv['config.schedule'] = config.schedule;
                }
                break;
            default:
        }
        return rv;
    };
    MonitorForm.prototype.render = function () {
        var _this = this;
        var monitor = this.props.monitor;
        var selectedProjectId = this.props.selection.projects[0];
        var selectedProject = selectedProjectId
            ? this.props.organization.projects.find(function (p) { return p.id === selectedProjectId + ''; })
            : null;
        return (<access_1.default access={['project:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<form_1.default allowUndo requireChanges apiEndpoint={_this.props.apiEndpoint} apiMethod={_this.props.apiMethod} model={_this.form} initialData={monitor
                        ? tslib_1.__assign({ name: monitor.name, type: monitor.type, project: monitor.project.slug }, _this.formDataFromConfig(monitor.type, monitor.config)) : {
                        project: selectedProject ? selectedProject.slug : null,
                    }} onSubmitSuccess={_this.props.onSubmitSuccess}>
            <panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Details')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                {monitor && (<field_1.default label={locale_1.t('ID')}>
                    <div className="controls">
                      <textCopyInput_1.default>{monitor.id}</textCopyInput_1.default>
                    </div>
                  </field_1.default>)}
                <selectField_1.default name="project" label={locale_1.t('Project')} disabled={!hasAccess} choices={_this.props.organization.projects
                        .filter(function (p) { return p.isMember; })
                        .map(function (p) { return [p.slug, p.slug]; })} required/>
                <textField_1.default name="name" placeholder={locale_1.t('My Cron Job')} label={locale_1.t('Name')} disabled={!hasAccess} required/>
              </panels_1.PanelBody>
            </panels_1.Panel>
            <panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Config')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                <selectField_1.default name="type" label={locale_1.t('Type')} disabled={!hasAccess} choices={MONITOR_TYPES} required/>
                <mobx_react_1.Observer>
                  {function () {
                        switch (_this.form.getValue('type')) {
                            case 'cron_job':
                                return (<react_1.Fragment>
                            <numberField_1.default name="config.max_runtime" label={locale_1.t('Max Runtime')} disabled={!hasAccess} help={locale_1.t("The maximum runtime (in minutes) a check-in is allowed before it's marked as a failure.")} placeholder="e.g. 30"/>
                            <selectField_1.default name="config.schedule_type" label={locale_1.t('Schedule Type')} disabled={!hasAccess} choices={SCHEDULE_TYPES} required/>
                          </react_1.Fragment>);
                            default:
                                return null;
                        }
                    }}
                </mobx_react_1.Observer>
                <mobx_react_1.Observer>
                  {function () {
                        switch (_this.form.getValue('config.schedule_type')) {
                            case 'crontab':
                                return (<react_1.Fragment>
                            <textField_1.default name="config.schedule" label={locale_1.t('Schedule')} disabled={!hasAccess} placeholder="*/5 * * * *" required help={locale_1.tct('Changes to the schedule will apply on the next check-in. See [link:Wikipedia] for crontab syntax.', {
                                        link: <a href="https://en.wikipedia.org/wiki/Cron"/>,
                                    })}/>
                            <numberField_1.default name="config.checkin_margin" label={locale_1.t('Check-in Margin')} disabled={!hasAccess} help={locale_1.t("The margin (in minutes) a check-in is allowed to exceed it's scheduled window before being treated as missed.")} placeholder="e.g. 30"/>
                          </react_1.Fragment>);
                            case 'interval':
                                return (<react_1.Fragment>
                            <numberField_1.default name="config.schedule.frequency" label={locale_1.t('Frequency')} disabled={!hasAccess} placeholder="e.g. 1" required/>
                            <selectField_1.default name="config.schedule.interval" label={locale_1.t('Interval')} disabled={!hasAccess} choices={INTERVALS} required/>
                            <numberField_1.default name="config.checkin_margin" label={locale_1.t('Check-in Margin')} disabled={!hasAccess} help={locale_1.t("The margin (in minutes) a check-in is allowed to exceed it's scheduled window before being treated as missed.")} placeholder="e.g. 30"/>
                          </react_1.Fragment>);
                            default:
                                return null;
                        }
                    }}
                </mobx_react_1.Observer>
              </panels_1.PanelBody>
            </panels_1.Panel>
          </form_1.default>);
            }}
      </access_1.default>);
    };
    return MonitorForm;
}(react_1.Component));
exports.default = withGlobalSelection_1.default(withOrganization_1.default(MonitorForm));
//# sourceMappingURL=monitorForm.jsx.map