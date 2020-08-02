/*!
FullCalendar List View Plugin v4.4.0
Docs & License: https://fullcalendar.io/
(c) 2019 Adam Shaw
*/(function(global,factory){typeof exports==='object'&&typeof module!=='undefined'?factory(exports,require('@fullcalendar/core')):typeof define==='function'&&define.amd?define(['exports','@fullcalendar/core'],factory):(global=global||self,factory(global.FullCalendarList={},global.FullCalendar));}(this,function(exports,core){'use strict';/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0
THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.
See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */var extendStatics=function(d,b){extendStatics=Object.setPrototypeOf||({__proto__:[]}instanceof Array&&function(d,b){d.__proto__=b;})||function(d,b){for(var p in b)if(b.hasOwnProperty(p))d[p]=b[p];};return extendStatics(d,b);};function __extends(d,b){extendStatics(d,b);function __(){this.constructor=d;}
d.prototype=b===null?Object.create(b):(__.prototype=b.prototype,new __());}
var ListEventRenderer=(function(_super){__extends(ListEventRenderer,_super);function ListEventRenderer(listView){var _this=_super.call(this)||this;_this.listView=listView;return _this;}
ListEventRenderer.prototype.attachSegs=function(segs){if(!segs.length){this.listView.renderEmptyMessage();}
else{this.listView.renderSegList(segs);}};ListEventRenderer.prototype.detachSegs=function(){};ListEventRenderer.prototype.renderSegHtml=function(seg){var _a=this.context,theme=_a.theme,options=_a.options;var eventRange=seg.eventRange;var eventDef=eventRange.def;var eventInstance=eventRange.instance;var eventUi=eventRange.ui;var url=eventDef.url;var classes=['fc-list-item'].concat(eventUi.classNames);var bgColor=eventUi.backgroundColor;var timeHtml;if(eventDef.allDay){timeHtml=core.getAllDayHtml(options);}
else if(core.isMultiDayRange(eventRange.range)){if(seg.isStart){timeHtml=core.htmlEscape(this._getTimeText(eventInstance.range.start,seg.end,false));}
else if(seg.isEnd){timeHtml=core.htmlEscape(this._getTimeText(seg.start,eventInstance.range.end,false));}
else{timeHtml=core.getAllDayHtml(options);}}
else{timeHtml=core.htmlEscape(this.getTimeText(eventRange));}
if(url){classes.push('fc-has-url');}
return '<tr class="'+classes.join(' ')+'">'+
(this.displayEventTime?'<td class="fc-list-item-time '+theme.getClass('widgetContent')+'">'+
(timeHtml||'')+
'</td>':'')+
'<td class="fc-list-item-marker '+theme.getClass('widgetContent')+'">'+
'<span class="fc-event-dot"'+
(bgColor?' style="background-color:'+bgColor+'"':'')+
'></span>'+
'</td>'+
'<td class="fc-list-item-title '+theme.getClass('widgetContent')+'">'+
'<a'+(url?' href="'+core.htmlEscape(url)+'"':'')+'>'+
core.htmlEscape(eventDef.title||'')+
'</a>'+
'</td>'+
'</tr>';};ListEventRenderer.prototype.computeEventTimeFormat=function(){return{hour:'numeric',minute:'2-digit',meridiem:'short'};};return ListEventRenderer;}(core.FgEventRenderer));var ListView=(function(_super){__extends(ListView,_super);function ListView(viewSpec,parentEl){var _this=_super.call(this,viewSpec,parentEl)||this;_this.computeDateVars=core.memoize(computeDateVars);_this.eventStoreToSegs=core.memoize(_this._eventStoreToSegs);_this.renderSkeleton=core.memoizeRendering(_this._renderSkeleton,_this._unrenderSkeleton);var eventRenderer=_this.eventRenderer=new ListEventRenderer(_this);_this.renderContent=core.memoizeRendering(eventRenderer.renderSegs.bind(eventRenderer),eventRenderer.unrender.bind(eventRenderer),[_this.renderSkeleton]);return _this;}
ListView.prototype.firstContext=function(context){context.calendar.registerInteractiveComponent(this,{el:this.el});};ListView.prototype.render=function(props,context){_super.prototype.render.call(this,props,context);var _a=this.computeDateVars(props.dateProfile),dayDates=_a.dayDates,dayRanges=_a.dayRanges;this.dayDates=dayDates;this.renderSkeleton(context);this.renderContent(context,this.eventStoreToSegs(props.eventStore,props.eventUiBases,dayRanges));};ListView.prototype.destroy=function(){_super.prototype.destroy.call(this);this.renderSkeleton.unrender();this.renderContent.unrender();this.context.calendar.unregisterInteractiveComponent(this);};ListView.prototype._renderSkeleton=function(context){var theme=context.theme;this.el.classList.add('fc-list-view');var listViewClassNames=(theme.getClass('listView')||'').split(' ');for(var _i=0,listViewClassNames_1=listViewClassNames;_i<listViewClassNames_1.length;_i++){var listViewClassName=listViewClassNames_1[_i];if(listViewClassName){this.el.classList.add(listViewClassName);}}
this.scroller=new core.ScrollComponent('hidden','auto');this.el.appendChild(this.scroller.el);this.contentEl=this.scroller.el;};ListView.prototype._unrenderSkeleton=function(){this.scroller.destroy();};ListView.prototype.updateSize=function(isResize,viewHeight,isAuto){_super.prototype.updateSize.call(this,isResize,viewHeight,isAuto);this.eventRenderer.computeSizes(isResize);this.eventRenderer.assignSizes(isResize);this.scroller.clear();if(!isAuto){this.scroller.setHeight(this.computeScrollerHeight(viewHeight));}};ListView.prototype.computeScrollerHeight=function(viewHeight){return viewHeight-
core.subtractInnerElHeight(this.el,this.scroller.el);};ListView.prototype._eventStoreToSegs=function(eventStore,eventUiBases,dayRanges){return this.eventRangesToSegs(core.sliceEventStore(eventStore,eventUiBases,this.props.dateProfile.activeRange,this.context.nextDayThreshold).fg,dayRanges);};ListView.prototype.eventRangesToSegs=function(eventRanges,dayRanges){var segs=[];for(var _i=0,eventRanges_1=eventRanges;_i<eventRanges_1.length;_i++){var eventRange=eventRanges_1[_i];segs.push.apply(segs,this.eventRangeToSegs(eventRange,dayRanges));}
return segs;};ListView.prototype.eventRangeToSegs=function(eventRange,dayRanges){var _a=this.context,dateEnv=_a.dateEnv,nextDayThreshold=_a.nextDayThreshold;var range=eventRange.range;var allDay=eventRange.def.allDay;var dayIndex;var segRange;var seg;var segs=[];for(dayIndex=0;dayIndex<dayRanges.length;dayIndex++){segRange=core.intersectRanges(range,dayRanges[dayIndex]);if(segRange){seg={component:this,eventRange:eventRange,start:segRange.start,end:segRange.end,isStart:eventRange.isStart&&segRange.start.valueOf()===range.start.valueOf(),isEnd:eventRange.isEnd&&segRange.end.valueOf()===range.end.valueOf(),dayIndex:dayIndex};segs.push(seg);if(!seg.isEnd&&!allDay&&dayIndex+1<dayRanges.length&&range.end<dateEnv.add(dayRanges[dayIndex+1].start,nextDayThreshold)){seg.end=range.end;seg.isEnd=true;break;}}}
return segs;};ListView.prototype.renderEmptyMessage=function(){this.contentEl.innerHTML='<div class="fc-list-empty-wrap2">'+
'<div class="fc-list-empty-wrap1">'+
'<div class="fc-list-empty">'+
core.htmlEscape(this.context.options.noEventsMessage)+
'</div>'+
'</div>'+
'</div>';};ListView.prototype.renderSegList=function(allSegs){var theme=this.context.theme;var segsByDay=this.groupSegsByDay(allSegs);var dayIndex;var daySegs;var i;var tableEl=core.htmlToElement('<table class="fc-list-table '+theme.getClass('tableList')+'"><tbody></tbody></table>');var tbodyEl=tableEl.querySelector('tbody');for(dayIndex=0;dayIndex<segsByDay.length;dayIndex++){daySegs=segsByDay[dayIndex];if(daySegs){tbodyEl.appendChild(this.buildDayHeaderRow(this.dayDates[dayIndex]));daySegs=this.eventRenderer.sortEventSegs(daySegs);for(i=0;i<daySegs.length;i++){tbodyEl.appendChild(daySegs[i].el);}}}
this.contentEl.innerHTML='';this.contentEl.appendChild(tableEl);};ListView.prototype.groupSegsByDay=function(segs){var segsByDay=[];var i;var seg;for(i=0;i<segs.length;i++){seg=segs[i];(segsByDay[seg.dayIndex]||(segsByDay[seg.dayIndex]=[])).push(seg);}
return segsByDay;};ListView.prototype.buildDayHeaderRow=function(dayDate){var _a=this.context,theme=_a.theme,dateEnv=_a.dateEnv,options=_a.options;var mainFormat=core.createFormatter(options.listDayFormat);var altFormat=core.createFormatter(options.listDayAltFormat);return core.createElement('tr',{className:'fc-list-heading','data-date':dateEnv.formatIso(dayDate,{omitTime:true})},'<td class="'+(theme.getClass('tableListHeading')||theme.getClass('widgetHeader'))+'" colspan="3">'+
(mainFormat?core.buildGotoAnchorHtml(options,dateEnv,dayDate,{'class':'fc-list-heading-main'},core.htmlEscape(dateEnv.format(dayDate,mainFormat))):'')+
(altFormat?core.buildGotoAnchorHtml(options,dateEnv,dayDate,{'class':'fc-list-heading-alt'},core.htmlEscape(dateEnv.format(dayDate,altFormat))):'')+
'</td>');};return ListView;}(core.View));ListView.prototype.fgSegSelector='.fc-list-item';function computeDateVars(dateProfile){var dayStart=core.startOfDay(dateProfile.renderRange.start);var viewEnd=dateProfile.renderRange.end;var dayDates=[];var dayRanges=[];while(dayStart<viewEnd){dayDates.push(dayStart);dayRanges.push({start:dayStart,end:core.addDays(dayStart,1)});dayStart=core.addDays(dayStart,1);}
return{dayDates:dayDates,dayRanges:dayRanges};}
var main=core.createPlugin({views:{list:{class:ListView,buttonTextKey:'list',listDayFormat:{month:'long',day:'numeric',year:'numeric'}},listDay:{type:'list',duration:{days:1},listDayFormat:{weekday:'long'}},listWeek:{type:'list',duration:{weeks:1},listDayFormat:{weekday:'long'},listDayAltFormat:{month:'long',day:'numeric',year:'numeric'}},listMonth:{type:'list',duration:{month:1},listDayAltFormat:{weekday:'long'}},listYear:{type:'list',duration:{year:1},listDayAltFormat:{weekday:'long'}}}});exports.ListView=ListView;exports.default=main;Object.defineProperty(exports,'__esModule',{value:true});}));