Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var actionLink_1 = tslib_1.__importDefault(require("app/components/actions/actionLink"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var customIgnoreCountModal_1 = tslib_1.__importDefault(require("app/components/customIgnoreCountModal"));
var customIgnoreDurationModal_1 = tslib_1.__importDefault(require("app/components/customIgnoreDurationModal"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var button_1 = tslib_1.__importDefault(require("./button"));
var menuHeader_1 = tslib_1.__importDefault(require("./menuHeader"));
var IGNORE_DURATIONS = [30, 120, 360, 60 * 24, 60 * 24 * 7];
var IGNORE_COUNTS = [1, 10, 100, 1000, 10000, 100000];
var IGNORE_WINDOWS = [
    [60, locale_1.t('per hour')],
    [24 * 60, locale_1.t('per day')],
    [24 * 7 * 60, locale_1.t('per week')],
];
var IgnoreActions = function (_a) {
    var onUpdate = _a.onUpdate, disabled = _a.disabled, shouldConfirm = _a.shouldConfirm, confirmMessage = _a.confirmMessage, _b = _a.confirmLabel, confirmLabel = _b === void 0 ? locale_1.t('Ignore') : _b, _c = _a.isIgnored, isIgnored = _c === void 0 ? false : _c;
    var onIgnore = function (statusDetails) {
        return onUpdate({
            status: types_1.ResolutionStatus.IGNORED,
            statusDetails: statusDetails || {},
        });
    };
    var onCustomIgnore = function (statusDetails) {
        onIgnore(statusDetails);
    };
    var actionLinkProps = {
        shouldConfirm: shouldConfirm,
        title: locale_1.t('Ignore'),
        message: confirmMessage,
        confirmLabel: confirmLabel,
        disabled: disabled,
    };
    if (isIgnored) {
        return (<tooltip_1.default title={locale_1.t('Change status to unresolved')}>
        <button_1.default priority="primary" onClick={function () { return onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED }); }} label={locale_1.t('Unignore')} icon={<icons_1.IconMute size="xs"/>}/>
      </tooltip_1.default>);
    }
    var openCustomIgnoreDuration = function () {
        return modal_1.openModal(function (deps) { return (<customIgnoreDurationModal_1.default {...deps} onSelected={function (details) { return onCustomIgnore(details); }}/>); });
    };
    var openCustomIngoreCount = function () {
        return modal_1.openModal(function (deps) { return (<customIgnoreCountModal_1.default {...deps} onSelected={function (details) { return onCustomIgnore(details); }} label={locale_1.t('Ignore this issue until it occurs again\u2026')} countLabel={locale_1.t('Number of times')} countName="ignoreCount" windowName="ignoreWindow" windowChoices={IGNORE_WINDOWS}/>); });
    };
    var openCustomIgnoreUserCount = function () {
        return modal_1.openModal(function (deps) { return (<customIgnoreCountModal_1.default {...deps} onSelected={function (details) { return onCustomIgnore(details); }} label={locale_1.t('Ignore this issue until it affects an additional\u2026')} countLabel={locale_1.t('Number of users')} countName="ignoreUserCount" windowName="ignoreUserWindow" windowChoices={IGNORE_WINDOWS}/>); });
    };
    return (<buttonBar_1.default merged>
      <actionLink_1.default {...actionLinkProps} type="button" title={locale_1.t('Ignore')} onAction={function () { return onUpdate({ status: types_1.ResolutionStatus.IGNORED }); }} icon={<icons_1.IconMute size="xs"/>}>
        {locale_1.t('Ignore')}
      </actionLink_1.default>
      <StyledDropdownLink customTitle={<button_1.default disabled={disabled} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>} alwaysRenderMenu disabled={disabled}>
        <menuHeader_1.default>{locale_1.t('Ignore')}</menuHeader_1.default>

        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {locale_1.t('For\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_DURATIONS.map(function (duration) { return (<DropdownMenuItem key={duration}>
                <StyledForActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreDuration: duration }); }}>
                  <ActionSubMenu>
                    <duration_1.default seconds={duration * 60}/>
                  </ActionSubMenu>
                </StyledForActionLink>
              </DropdownMenuItem>); })}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIgnoreDuration}>{locale_1.t('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>

        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {locale_1.t('Until this occurs again\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_COUNTS.map(function (count) { return (<DropdownMenuItem key={count}>
                <dropdownLink_1.default title={<ActionSubMenu>
                      {count === 1
                    ? locale_1.t('one time\u2026') // This is intentional as unbalanced string formatters are problematic
                    : locale_1.tn('%s time\u2026', '%s times\u2026', count)}
                      <SubMenuChevron>
                        <icons_1.IconChevron direction="right" size="xs"/>
                      </SubMenuChevron>
                    </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                  <DropdownMenuItem>
                    <StyledActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreCount: count }); }}>
                      {locale_1.t('from now')}
                    </StyledActionLink>
                  </DropdownMenuItem>
                  {IGNORE_WINDOWS.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), hours = _b[0], label = _b[1];
                return (<DropdownMenuItem key={hours}>
                      <StyledActionLink {...actionLinkProps} onAction={function () {
                        return onIgnore({
                            ignoreCount: count,
                            ignoreWindow: hours,
                        });
                    }}>
                        {label}
                      </StyledActionLink>
                    </DropdownMenuItem>);
            })}
                </dropdownLink_1.default>
              </DropdownMenuItem>); })}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIngoreCount}>{locale_1.t('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <dropdownLink_1.default title={<ActionSubMenu>
                {locale_1.t('Until this affects an additional\u2026')}
                <SubMenuChevron>
                  <icons_1.IconChevron direction="right" size="xs"/>
                </SubMenuChevron>
              </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
            {IGNORE_COUNTS.map(function (count) { return (<DropdownMenuItem key={count}>
                <dropdownLink_1.default title={<ActionSubMenu>
                      {locale_1.tn('one user\u2026', '%s users\u2026', count)}
                      <SubMenuChevron>
                        <icons_1.IconChevron direction="right" size="xs"/>
                      </SubMenuChevron>
                    </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                  <DropdownMenuItem>
                    <StyledActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreUserCount: count }); }}>
                      {locale_1.t('from now')}
                    </StyledActionLink>
                  </DropdownMenuItem>
                  {IGNORE_WINDOWS.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), hours = _b[0], label = _b[1];
                return (<DropdownMenuItem key={hours}>
                      <StyledActionLink {...actionLinkProps} onAction={function () {
                        return onIgnore({
                            ignoreUserCount: count,
                            ignoreUserWindow: hours,
                        });
                    }}>
                        {label}
                      </StyledActionLink>
                    </DropdownMenuItem>);
            })}
                </dropdownLink_1.default>
              </DropdownMenuItem>); })}
            <DropdownMenuItem>
              <ActionSubMenu>
                <a onClick={openCustomIgnoreUserCount}>{locale_1.t('Custom')}</a>
              </ActionSubMenu>
            </DropdownMenuItem>
          </dropdownLink_1.default>
        </DropdownMenuItem>
      </StyledDropdownLink>
    </buttonBar_1.default>);
};
exports.default = IgnoreActions;
var actionLinkCss = function (p) { return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", " !important;\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", " !important;\n  }\n"])), p.theme.subText, p.theme.borderRadius, p.theme.bodyBackground); };
var StyledActionLink = styled_1.default(actionLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: 7px 10px !important;\n  ", ";\n"], ["\n  padding: 7px 10px !important;\n  ", ";\n"])), actionLinkCss);
var StyledForActionLink = styled_1.default(actionLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: ", " 0;\n  ", ";\n"], ["\n  padding: ", " 0;\n  ", ";\n"])), space_1.default(0.5), actionLinkCss);
var StyledDropdownLink = styled_1.default(dropdownLink_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"], ["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"])));
var DropdownMenuItem = styled_1.default('li')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  :not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n  > span {\n    display: block;\n    > ul {\n      border-radius: ", ";\n      top: 5px;\n      left: 100%;\n      margin-top: -5px;\n      margin-left: -1px;\n      &:after,\n      &:before {\n        display: none !important;\n      }\n    }\n  }\n  &:hover > span {\n    background: ", ";\n  }\n"], ["\n  :not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n  > span {\n    display: block;\n    > ul {\n      border-radius: ", ";\n      top: 5px;\n      left: 100%;\n      margin-top: -5px;\n      margin-left: -1px;\n      &:after,\n      &:before {\n        display: none !important;\n      }\n    }\n  }\n  &:hover > span {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.focus; });
var ActionSubMenu = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  grid-column-start: 1;\n  grid-column-end: 4;\n  gap: ", ";\n  padding: ", " 0;\n  color: ", ";\n  a {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  grid-column-start: 1;\n  grid-column-end: 4;\n  gap: ", ";\n  padding: ", " 0;\n  color: ", ";\n  a {\n    color: ", ";\n  }\n"])), space_1.default(1), space_1.default(0.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var SubMenuChevron = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-self: center;\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  align-self: center;\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=ignore.jsx.map