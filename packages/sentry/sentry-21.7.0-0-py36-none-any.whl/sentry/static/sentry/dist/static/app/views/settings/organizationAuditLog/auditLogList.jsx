Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var selectField_1 = tslib_1.__importDefault(require("app/components/forms/selectField"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var avatarStyle = {
    width: 36,
    height: 36,
    marginRight: 8,
};
var AuditLogList = function (_a) {
    var pageLinks = _a.pageLinks, entries = _a.entries, eventType = _a.eventType, eventTypes = _a.eventTypes, onEventSelect = _a.onEventSelect;
    var hasEntries = entries && entries.length > 0;
    var ipv4Length = 15;
    var options = tslib_1.__spreadArray([
        { value: '', label: locale_1.t('Any action'), clearableVaue: false }
    ], tslib_1.__read(eventTypes.map(function (type) { return ({ label: type, value: type, clearableValue: false }); })));
    var action = (<form>
      <selectField_1.default name="event" onChange={onEventSelect} value={eventType} style={{ width: 250 }} options={options}/>
    </form>);
    return (<div>
      <settingsPageHeader_1.default title={locale_1.t('Audit Log')} action={action}/>
      <panels_1.Panel>
        <StyledPanelHeader disablePadding>
          <div>{locale_1.t('Member')}</div>
          <div>{locale_1.t('Action')}</div>
          <div>{locale_1.t('IP')}</div>
          <div>{locale_1.t('Time')}</div>
        </StyledPanelHeader>

        <panels_1.PanelBody>
          {!hasEntries && <emptyMessage_1.default>{locale_1.t('No audit entries available')}</emptyMessage_1.default>}

          {hasEntries &&
            entries.map(function (entry) { return (<StyledPanelItem center key={entry.id}>
                <UserInfo>
                  <div>
                    {entry.actor.email && (<userAvatar_1.default style={avatarStyle} user={entry.actor}/>)}
                  </div>
                  <NameContainer>
                    <Name data-test-id="actor-name">
                      {entry.actor.isSuperuser
                    ? locale_1.t('%s (Sentry Staff)', entry.actor.name)
                    : entry.actor.name}
                    </Name>
                    <Note>{entry.note}</Note>
                  </NameContainer>
                </UserInfo>
                <div>
                  <MonoDetail>{entry.event}</MonoDetail>
                </div>
                <TimestampOverflow>
                  <tooltip_1.default title={entry.ipAddress} disabled={entry.ipAddress && entry.ipAddress.length <= ipv4Length}>
                    <MonoDetail>{entry.ipAddress}</MonoDetail>
                  </tooltip_1.default>
                </TimestampOverflow>
                <TimestampInfo>
                  <dateTime_1.default dateOnly date={entry.dateCreated}/>
                  <dateTime_1.default timeOnly format="LT zz" date={entry.dateCreated}/>
                </TimestampInfo>
              </StyledPanelItem>); })}
        </panels_1.PanelBody>
      </panels_1.Panel>
      {pageLinks && <pagination_1.default pageLinks={pageLinks}/>}
    </div>);
};
var UserInfo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  line-height: 1.2;\n  font-size: 13px;\n  flex: 1;\n"], ["\n  display: flex;\n  line-height: 1.2;\n  font-size: 13px;\n  flex: 1;\n"])));
var NameContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"])));
var Name = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: 600;\n  font-size: 15px;\n"], ["\n  font-weight: 600;\n  font-size: 15px;\n"])));
var Note = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  word-break: break-word;\n"], ["\n  font-size: 13px;\n  word-break: break-word;\n"])));
var TimestampOverflow = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis_1.default);
var MonoDetail = styled_1.default('code')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledPanelHeader = styled_1.default(panels_1.PanelHeader)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"])), space_1.default(2), space_1.default(2));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"])), space_1.default(2), space_1.default(2));
var TimestampInfo = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; });
exports.default = AuditLogList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=auditLogList.jsx.map